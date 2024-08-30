import pytest
from pyparsing.exceptions import ParseException

from ..expressions import (
    Array,
    ASTNode,
    BinOp,
    Element,
    Function,
    Property,
    RightOp,
    expression,
)


def test_schema_expressions(schema_obj):
    # Basic smoke test. All of these expressions should parse without error.
    for testexp in schema_obj.meta.expression_tests:
        expression.parse_string(testexp["expression"])


@pytest.mark.parametrize(
    "expr, disambiguated",
    [
        ("a*x**2 + b*x + c == 0", "((((a * (x ** 2)) + (b * x)) + c) == 0)"),
        ("a.b.c[0][1][2].d(3, 4)", "(((a.b).c)[0][1][2].d)(3, 4)"),
        (
            "nifti_header.pixdim[4] == sidecar.RepetitionTime",
            "((nifti_header.pixdim)[4] == (sidecar.RepetitionTime))",
        ),
        (
            """x.y * 10 ** (-3 * index(["a", "b", "c"], w.z))""",
            """((x.y) * (10 ** (-3 * index(['"a"', '"b"', '"c"'], (w.z)))))""",
        ),
        ("a && b && c || d || e && f", "((a && (b && c)) || (d || (e && f)))"),
        ("! a && b || ! c == d || e", "(((!a) && b) || ((!(c == d)) || e))"),
    ],
)
def test_expression_associations(expr, disambiguated):
    # The goal of this test is to use the str() function on the AST to
    # reproduce the original expression, but with parentheses demonstrating
    # associativity. For example `a.b.c` could be parsed `(a.b).c` or `a.(b.c)`.
    parse_results = expression.parse_string(expr)
    assert len(parse_results) == 1
    ast = parse_results[0]
    assert str(ast) == disambiguated


def test_selectors(schema_obj):
    # Selectors happen at the second level in a file
    # For directories of files, need to look three down
    for rules, level in (
        (schema_obj.rules.checks, 3),
        (schema_obj.rules.dataset_metadata, 2),
        (schema_obj.rules.sidecars, 3),
        (schema_obj.rules.tabular_data, 3),
        (schema_obj.rules.errors, 2),
    ):
        keys = (key for key in rules.keys(level=level) if key.endswith("selectors"))
        for key in keys:
            for selector in rules[key]:
                ast = expression.parse_string(selector)[0]
                assert isinstance(ast, ASTNode)


def test_checks(schema_obj):
    checks = (
        expr
        for key, value in schema_obj.rules.checks.items(level=3)
        if key.endswith("checks")
        for expr in value
    )
    for check in checks:
        ast = expression.parse_string(check)[0]
        assert isinstance(ast, ASTNode)


@pytest.mark.parametrize(
    "expr",
    (
        "func(x, y",
        "lhs == ",
        "assignment = not.a.thing",
    ),
)
def test_expected_failures(expr):
    with pytest.raises(ParseException):
        expression.parse_string(expr)


def test_valid_sidecar_field(schema_obj):
    """Check sidecar fields actually exist in the metadata listed in the schema.

    Test failures are usually due to typos.
    """
    for rules, level in ((schema_obj.rules.checks, 3),):
        keys = (key for key in rules.keys(level=level) if key.endswith("selectors"))
        check_fields(schema_obj, rules, keys)

        keys = (key for key in rules.keys(level=level) if key.endswith("checks"))
        check_fields(schema_obj, rules, keys)


def check_fields(schema_obj, rules, keys):
    for key in keys:
        for rule in rules[key]:
            ast = expression.parse_string(rule)[0]
            if isinstance(ast, BinOp):
                check_binop(schema_obj, ast)
            elif isinstance(ast, Function):
                check_function(schema_obj, ast)
            elif isinstance(ast, Property):
                check_property(schema_obj, ast)
            elif isinstance(ast, RightOp):
                check_half(schema_obj, ast.rh)


def check_binop(schema_obj, binop):
    for half in [binop.lh, binop.rh]:
        check_half(schema_obj, half)


def check_half(schema_obj, half):
    if isinstance(half, BinOp):
        check_binop(schema_obj, half)
    elif isinstance(half, Function):
        check_function(schema_obj, half)
    elif isinstance(half, Property):
        check_property(schema_obj, half)
    elif isinstance(half, Element):
        check_property(schema_obj, half.name)


def check_function(schema_obj, function):
    for x in function.args:
        if isinstance(x, Property):
            check_property(schema_obj, x)
        elif isinstance(x, Function):
            check_function(schema_obj, x)
        elif isinstance(x, Array):
            check_array(schema_obj, x)


def check_array(schema_obj, array):
    for element in array.elements:
        if isinstance(element, Property):
            check_property(schema_obj, element)


def check_property(schema_obj, property):
    if property.name == "sidecar":
        assert property.field in schema_obj.objects.metadata
