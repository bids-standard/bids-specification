from pyparsing import (
    Forward,
    Group,
    Literal,
    Optional,
    StringEnd,
    StringStart,
    Suppress,
    ZeroOrMore,
    common,
    delimited_list,
    one_of,
    quoted_string,
)

# EBNF-ish grammar
#
# # In order of binding (loosest to tightest)
# cmpOp :: '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in'
# orOp  :: '||'
# andOp :: '&&'
# notOp :: '!'
# addOp :: '+' | '-'
# mulOp :: '*' | '/' | '%'
# expOp :: '**'
#
# item    :: '(' test ')' | '[' [testList] '] | '{' '}' | NAME | NUMBER | STRING
# trailer :: '(' [testList] ') | '[' testList ']' | '.' NAME
# atom    :: item trailer*
#
# ## Alternative: (possibly with 'null' as additional literal)
# ## This makes things like '1(a, b, c)' or '"string"[0]' syntax errors
# # literal :: NUMBER | STRING
# # item    :: '(' test ')' | '[' testList '] | NAME
# # atom    :: literal | item trailer*
#
# factor :: atom [ expOp factor ]*
# term   :: factor [ mulOp factor ]*
# expr   :: term [ addOp term ]*
#
# comparison :: expr [ compOp expr ]*
# notTest    :: not notTest | comparison
# andTest    :: notTest [ '&&' andTest ]*
# test       :: andTest [ '||' test ]*
#
# testList   :: test [ ',' testList ]*
#
# expression :: ^ test $

compOp = one_of(("==", "!=", "<", "<=", ">", ">=", "in"))
orOp = Literal("||")
andOp = Literal("&&")
notOp = Literal("!")
addOp = one_of(("+", "-"))
mulOp = one_of(("*", "/"))
expOp = Literal("**")

lpar, rpar = map(Suppress, "()")
lsqr, rsqr = map(Suppress, "[]")
lcur, rcur = map(Suppress, "{}")

# Recursively-defined expressions
factor = Forward()
term = Forward()
expr = Forward()
comparison = Forward()
notTest = Forward()
andTest = Forward()
test = Forward()

testlist = delimited_list(test)

# Numbers and strings are base types, this could be expanded with bools and null
# if it seems useful
literal = common.number | quoted_string
# Items are units that operations can be done on, including arithmetic, comparison,
# function calls, index lookups and attribute lookups
item = (
    Group(lpar + test + rpar)
    | Group(lsqr + Optional(testlist) + rsqr)("array")
    # If object literals ever occur in real expressions, we'll need to define this
    | Group(lcur + rcur)("empty object")
    | common.identifier
    | literal
)
# Trailers are function calls, array indexes, and object attributes
trailer = (
    Group(lpar + Optional(testlist) + rpar)("args")
    | Group(lsqr + test + rsqr)("index")
    | Group(Literal(".") + common.identifier)("attr")
)
# An atom might have some lookups done, but now it can be part of an arithmetic
# expression
atom = item + ZeroOrMore(trailer)

# Arithmetic expressions
factor <<= atom + ZeroOrMore(Group(expOp + factor))
term <<= factor + ZeroOrMore(Group(mulOp + term))
expr <<= term + ZeroOrMore(Group(addOp + expr))

# Logic expressions (tests, to avoid name collision)
comparison <<= expr + ZeroOrMore(Group(compOp + comparison))
notTest <<= notOp + notTest | comparison
andTest <<= notTest + ZeroOrMore(Group(andOp + andTest))
test <<= andTest + ZeroOrMore(Group(orOp + test))

# Schema expressions must parse from start to finish
expression = StringStart() + test + StringEnd()
