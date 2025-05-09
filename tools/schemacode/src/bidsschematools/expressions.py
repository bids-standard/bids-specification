"""Parsing utilities for BIDS Schema expression language"""

from functools import partial

from pyparsing import (
    Forward,
    Literal,
    Optional,
    StringEnd,
    StringStart,
    Suppress,
    common,
    delimited_list,
    one_of,
    quoted_string,
)


def parse(expression_string: str) -> "ASTNode":
    """Convert a BIDS schema expression into an abstract syntax tree

    EBNF-ish grammar::

        # In order of binding (loosest to tightest)
        orOp  :: '||'
        andOp :: '&&'
        notOp :: '!'
        cmpOp :: '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in'
        addOp :: '+' | '-'
        mulOp :: '*' | '/' | '%'
        expOp :: '**'

        item    :: '(' test ')' | '[' [testList] '] | '{' '}' | NAME | NUMBER | STRING
        trailer :: '(' [testList] ') | '[' test ']' | '.' NAME
        atom    :: item trailer*

        factor :: atom [ expOp factor ]*
        term   :: factor [ mulOp factor ]*
        expr   :: term [ addOp term ]*

        comparison :: expr [ compOp expr ]*
        notTest    :: not notTest | comparison
        andTest    :: notTest [ '&&' andTest ]*
        test       :: andTest [ '||' test ]*

        testList   :: test [ ',' test ]*

        expression :: ^ test $
    """
    # Alternative: (possibly with 'null' as additional literal)
    # This makes things like '1(a, b, c)' or '"string"[0]' syntax errors
    #
    # literal :: NUMBER | STRING
    # item    :: '(' test ')' | '[' testList '] | NAME
    # atom    :: literal | item trailer*

    return expression.parse_string(expression_string)[0]


orOp = Literal("||")
andOp = Literal("&&")
notOp = Literal("!")
compOp = one_of(("==", "!=", "<", "<=", ">", ">=", "in"))
addOp = one_of(("+", "-"))
mulOp = one_of(("*", "/"))
expOp = Literal("**")

lpar, rpar = Suppress("("), Suppress(")")
lsqr, rsqr = Suppress("["), Suppress("]")
dot = Suppress(".")

# Right-associative expressions need to be recursively defined
factor = Forward()
notTest = Forward()
andTest = Forward()
test = Forward()

testlist = delimited_list(test)

# Numbers and strings are base types, this could be expanded with bools and null
# if it seems useful
literal = common.number | quoted_string

# Items are units that operations can be done on, including arithmetic, comparison,
# function calls, index lookups and attribute lookups
array = lsqr + Optional(testlist) + rsqr
parenthetical = lpar + test + rpar
# If object literals ever occur in real expressions, we'll need to define this
obj_literal = Literal("{}")
item = parenthetical | array | obj_literal | common.identifier | literal

# Trailers are function calls, array indexes, and object attributes
function_call = lpar + Optional(testlist) + rpar
array_lookup = lsqr + test + rsqr
object_lookup = dot + common.identifier
trailer = function_call | array_lookup | object_lookup

# An atom might have some lookups done, but now it can be part of an arithmetic
# expression
atom = item + (trailer)[...]

# Arithmetic expressions
factor <<= atom + (expOp + factor)[...]  # Right-associative
term = factor + (mulOp + factor)[...]
expr = term + (addOp + term)[...]

# Logic expressions (tests, to avoid name collision)
comparison = expr + (compOp + expr)[...]
notTest <<= notOp + notTest | comparison
andTest <<= notTest + (andOp + andTest)[...]  # Right-associative
test <<= andTest + (orOp + test)[...]  # Right-associative

# Schema expressions must parse from start to finish
expression = StringStart() + test + StringEnd()


# With the grammar defined, we need the following syntax elements
class ASTNode:
    """AST superclass

    Defines basic repr. Subclasses should define __str__ with enough
    parentheses to make associations unambiguous.
    """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__dict__}>"

    def __str__(self) -> str:
        raise NotImplementedError


class RightOp(ASTNode):
    """Right-associative unary operator"""

    def __init__(self, tokens):
        self.op, self.rh = tokens

    def __str__(self):
        return f"({self.op}{self.rh})"

    @classmethod
    def maybe(cls, tokens):
        """Construct class only if not degenerate"""
        if len(tokens) < 2:
            return tokens
        return cls(tokens)


class BinOp(ASTNode):
    """Binary operator"""

    def __init__(self, tokens):
        self.lh, self.op, self.rh = tokens

    @classmethod
    def maybe(cls, tokens):
        """Construct class if not degenerate

        * Right-associative: ``outer <<= inner + (op + outer)[...]``
        * Left-associative: ``outer = inner + (op + inner)[...]``

        In the right-associative case, we get ``[inner, op, BinOp(outer)]``,
        so we loop once and are done.

        In the left-associative case, we get ``[inner, op, inner, op, ...]``,
        convert to ``[BinOp(inner, op, inner), op, inner, ...]``
        """
        while len(tokens) >= 3:
            tokens = [cls(tokens[:3])] + tokens[3:]
        return tokens

    def __str__(self):
        return f"({self.lh} {self.op} {self.rh})"


class Function(ASTNode):
    """Function call"""

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        arglist = ", ".join(map(str, self.args))
        return f"{self.name}({arglist})"


class Element(ASTNode):
    """Array element lookup"""

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __str__(self):
        return f"{self.name}[{self.index}]"


class Property(ASTNode):
    """Object property lookup"""

    def __init__(self, name, field):
        self.name = name
        self.field = field

    def __str__(self):
        return f"({self.name}.{self.field})"


class Array(ASTNode):
    """Array literal"""

    def __init__(self, tokens):
        self.elements = list(tokens)

    def __str__(self):
        return str(self.elements)


class Object(ASTNode):
    """Object literal, unused outside tests, so degenerate"""

    def __init__(self, tokens):
        pass

    def __str__(self):
        return "{}"


array.set_parse_action(Array)
obj_literal.set_parse_action(Object)

# Function calls and item lookups need to be constructed partially
function_call.set_parse_action(lambda t: partial(Function, args=list(t)))
array_lookup.set_parse_action(lambda t: partial(Element, index=t[0]))
object_lookup.set_parse_action(lambda t: partial(Property, field=t[0]))


# Once the atom is complete, we can build the left-associative tree by completing application
def atomize(tokens):
    item = tokens.pop(0)
    for trailer in tokens:
        item = trailer(item)
    return item


atom.set_parse_action(atomize)

# Arithmetic expressions can all be degenerate, so use maybe to pass through
factor.set_parse_action(BinOp.maybe)
term.set_parse_action(BinOp.maybe)
expr.set_parse_action(BinOp.maybe)

comparison.set_parse_action(BinOp.maybe)
notTest.set_parse_action(RightOp.maybe)
andTest.set_parse_action(BinOp.maybe)
test.set_parse_action(BinOp.maybe)
