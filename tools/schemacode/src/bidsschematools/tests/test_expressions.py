from __future__ import annotations

from collections.abc import Mapping
from functools import singledispatch

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
from ..types import Namespace


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


def walk_schema(schema_obj, predicate):
    for key, value in schema_obj.items():
        if predicate(key, value):
            yield key, value
        if isinstance(value, Mapping):
            for subkey, value in walk_schema(value, predicate):
                yield f"{key}.{subkey}", value


def test_valid_sidecar_field(schema_obj):
    """Check sidecar fields actually exist in the metadata listed in the schema.

    Test failures are usually due to typos.
    """
    field_names = {field.name for key, field in schema_obj.objects.metadata.items()}

    for key, rule in walk_schema(
        schema_obj.rules, lambda k, v: isinstance(v, Mapping) and v.get("selectors")
    ):
        for selector in rule["selectors"]:
            ast = expression.parse_string(selector)[0]
            for name in find_names(ast):
                if name.startswith(("json.", "sidecar.")):
                    assert name.split(".", 1)[1] in field_names, (
                        f"Bad field in selector: {name} ({key})"
                    )
        for check in rule.get("checks", []):
            ast = expression.parse_string(check)[0]
            for name in find_names(ast):
                if name.startswith(("json.", "sidecar.")):
                    assert name.split(".", 1)[1] in field_names, (
                        f"Bad field in check: {name} ({key})"
                    )


def test_test_valid_sidecar_field():
    schema_obj = Namespace.build(
        {
            "objects": {
                "metadata": {
                    "a": {"name": "a"},
                }
            },
            "rules": {"myruleA": {"selectors": ["sidecar.a"], "checks": ["json.a == sidecar.a"]}},
        }
    )
    test_valid_sidecar_field(schema_obj)

    schema_obj.objects.metadata.a["name"] = "b"
    with pytest.raises(AssertionError):
        test_valid_sidecar_field(schema_obj)


@singledispatch
def find_names(node: ASTNode | str):
    # Walk AST nodes
    if isinstance(node, BinOp):
        yield from find_names(node.lh)
        yield from find_names(node.rh)
    elif isinstance(node, RightOp):
        yield from find_names(node.rh)
    elif isinstance(node, Array):
        for element in node.elements:
            yield from find_names(element)
    elif isinstance(node, Element):
        yield from find_names(node.name)
        yield from find_names(node.index)
    elif isinstance(node, (int, float)):
        return
    else:
        raise TypeError(f"Unexpected node type: {node!r}")


@find_names.register
def find_function_names(node: Function):
    yield node.name
    for arg in node.args:
        yield from find_names(arg)


@find_names.register
def find_property_name(node: Property):
    # Properties are left-associative, so expand the left side
    yield f"{next(find_names(node.name))}.{node.field}"


@find_names.register
def find_identifiers(node: str):
    if not node.startswith(('"', "'")):
        yield node
