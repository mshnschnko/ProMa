from enum import Enum


class Terminal(Enum):
    word = "word"
    char_sequence = "char_sequence"
    other = "other"


tokenRegularExpressions = [
    (Terminal.word, r'[\[\]a-zA-Z0-9_+*/\-=\. ]+'),
    (Terminal.char_sequence, r"[\(\),:]"),
    (Terminal.other, r"(?:(@@\{))[ \t]*(.*?)[ \t]*(?(2)\})"),
]


keys = [
    ("algorithm", Terminal.word),
    ("return", Terminal.word),
    ("yield", Terminal.word),
    ("call", Terminal.word),
    ("func", Terminal.word),
    ("proc", Terminal.word),
    ("iter", Terminal.word),
    ("end func", Terminal.word),
    ("end proc", Terminal.word),
    ("end iter", Terminal.word),
    ("assign", Terminal.word),
    ("next for", Terminal.word),
    ("exit for", Terminal.word),
    ("goto", Terminal.word),
    ("define", Terminal.word),
    ("comment", Terminal.word),
    ("integer", Terminal.word),
    ("string", Terminal.word),
    ("char", Terminal.word),
    ("array", Terminal.word),
    ("struct", Terminal.word),
    ("if", Terminal.word),
    ("end if", Terminal.word),
    ("for", Terminal.word),
    ("end for", Terminal.word),
    ("while", Terminal.word),
    ("end while", Terminal.word),
    ("repeat", Terminal.word),
    (",", Terminal.char_sequence),
    ("(", Terminal.char_sequence),
    (")", Terminal.char_sequence),
    (":", Terminal.char_sequence),
]


class Nonterminal(Enum):
    DEFINITION = 'DEFINITION'
    INPUT = 'INPUT'
    ASSIGNMENT = 'ASSIGNMENT'
    ALG_UNIT = 'ALG_UNIT'
    WHILE = 'WHILE'
    CALL = 'CALL'
    FLOW_STRUCTURE = 'FLOW_STRUCTURE'
    FRAGMENT = 'FRAGMENT'
    REPEAT = 'REPEAT'
    RETURN = 'RETURN'
    CODE_BLOCK = 'CODE_BLOCK'
    OUTPUT = 'OUTPUT'
    ALG_OUTPUT = 'ALG_OUTPUT'
    BRANCHING = 'BRANCHING'
    FOR = 'FOR'
    YIELD = 'YIELD'
    NAME = 'NAME'
    UNIT_NAME = 'UNIT_NAME'
    COMMENT = 'COMMENT'
    S = 'S'
    ALG = 'ALG'
    CYCLE = 'CYCLE'
    ALG_UNIT_RETURN = 'ALG_UNIT_RETURN'
    OPERATOR = 'OPERATOR'
    TYPE = 'TYPE'
    TYPE_ARRAY = 'TYPE_ARRAY'
    TYPE_STRUCT = 'TYPE_STRUCT'
    TRANSITION = 'TRANSITION'
    PARAM_LIST = 'PARAM_LIST'
    STATEMENT = 'STATEMENT'


axiom = Nonterminal.S
