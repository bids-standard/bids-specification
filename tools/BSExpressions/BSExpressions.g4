grammar BSExpressions;

// Define tokens
OR_OP : '||';
AND_OP : '&&';
NOT_OP : '!';
COMP_OP : '==' | '!=' | '<' | '<=' | '>' | '>=';
ADD_OP : '+' | '-';
MUL_OP : '*' | '/';
EXP_OP : '**';
LPAR : '(';
RPAR : ')';
LSQR : '[';
RSQR : ']';
DOT : '.';

// Define literals
LITERAL : (NUMBER | QUOTED_STRING);
NUMBER : INT | FLOAT;
INT : ('+' | '-')? DIGIT+;
FLOAT : ('+' | '-')? DIGIT+ '.' DIGIT+;
DIGIT : [0-9];
QUOTED_STRING : '"' (ESC | ~["\\])* '"';
ESC : '\\' ["\\/bfnrt];
BOOL : 'True' | 'False';
NULL : 'None';

// Define rules
start : expression EOF;

expression : test;

test : andTest (OR_OP andTest)*;

andTest : notTest (AND_OP notTest)*;

notTest : NOT_OP notTest | comparison;

comparison : expr (COMP_OP expr)*;

expr : term (ADD_OP term)*;

term : factor (MUL_OP factor)*;

factor : atom (EXP_OP factor)?;

atom : item (trailer)*;

item : parenthetical | array | obj_literal | identifier | LITERAL;

parenthetical : LPAR test RPAR;

array : LSQR (test (',' test)*)? RSQR;

obj_literal : '{}';

trailer : function_call | array_lookup | object_lookup;

function_call : LPAR (test (',' test)*)? RPAR;

array_lookup : LSQR test RSQR;

object_lookup : DOT identifier;

identifier : IDENT_START IDENT_PART*;

fragment IDENT_START : [a-zA-Z_];
fragment IDENT_PART : [a-zA-Z_0-9];

WS : [ \t\r\n]+ -> skip;
