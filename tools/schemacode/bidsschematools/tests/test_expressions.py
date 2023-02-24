import pytest

from ..expressions import expression


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
