import pytest
from pyparsing.exceptions import ParseException

from ..expressions import ASTNode, expression


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
