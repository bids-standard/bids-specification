from ..expressions import expression


def test_schema_expressions(schema_obj):
    # Basic smoke test. All of these expressions should parse without error.
    for testexp in schema_obj.meta.expression_tests:
        expression.parse_string(testexp["expression"])
