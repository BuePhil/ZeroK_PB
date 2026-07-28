from ply.lex import lex

reserve = (
    'if',
    'else',
    'until',
    'do',
    'done',
    'onbreak',
    'break',
    'continue',
    'elif',
    'print',
    'with',
    'func',
    'return',
    'get',
    'list'
)

reserved = {i:i.upper() for i in reserve}

tokens = [
    'NEWLINE',
    'COMMENT',
    'TYPE',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'AND_BIT',
    'OR_BIT',
    'MOD',
    'XOR_BIT',
    'NOT_BIT',
    'SMALLER',
    'GREATER',
    'EQUALS',
    'SMALLER_EQ',
    'GREATER_EQ',
    'NOT_EQ',
    'AND_BOOL',
    'OR_BOOL',
    'XOR_BOOL',
    'NOT_BOOL',
    'BOOLEAN',
    'LASSIGN',
    'RASSIGN',
    'IDENTIFIER',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'HASH',
    'FUNCARROW',
    'COMMA',
    'CHAR',
    'STRING',
    'SEMICOLON',
    'DOT',
    'LBRACKET',
    'RBRACKET',
    'INDEX'
] + list(reserved.values())

#t_NUMBER = r'\d+'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_AND_BIT = r'\&'
t_OR_BIT = r'\|'
t_MOD = r'\%'
t_XOR_BIT = r'\^'
t_NOT_BIT = r'\!'
t_SMALLER = r'\<'
t_GREATER = r'\>'
t_EQUALS = r'\='
t_SMALLER_EQ = r'\<\='
t_GREATER_EQ = r'\>\='
t_NOT_EQ = r'\!\='
t_AND_BOOL = r'\&\&'
t_OR_BOOL = r'\|\|'
t_XOR_BOOL = r'\^\^'
t_NOT_BOOL = r'\!\!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HASH = r'\#'
t_LASSIGN = r'\<\-'
t_RASSIGN = r'\-\>'
t_FUNCARROW = r'\=\>'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

bases = {
    'b' : 2,
    's' : 6,
    'o' : 8,
    'd' : 10,
    'x' : 16
}

def t_NEWLINE(t):
    r'\n+'
    pass

def t_CHAR(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_TYPE(t):
    r'(int|bool|string|char)\b'
    #t.type = reserved.get(t.value, 'TYPE')
    return t

def t_NUMBER(t):
    r'(([01]+b|[0-5]+s|[0-7]+o|[0-9]+d|[0-9a-fA-F]+x)(u|s))\b'

    n, b, ty = (str.lower() for str in [t.value[:-2], t.value[-2], t.value[-1]])
    t.value = (n, bases[b], ty)
    return t

def t_INDEX(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'(true|True|TRUE|TT|tt|T|t)\b'
    return t

def t_IDENTIFIER(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_COMMENT(t):
    r'\(:[\s\S]*?:\)'
    pass

t_ignore  = ' \t'

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")

lexer = lex()