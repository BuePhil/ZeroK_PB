from ply.yacc import yacc
from ice_lexer import tokens

precedence = [
    ('left', 'PLUS', 'MINUS'),
    ('left', 'AND_BIT', 'OR_BIT', 'XOR_BIT', 'AND_BOOL', 'OR_BOOL', 'XOR_BOOL'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT_BIT', 'NOT_BOOL'),
    ('left', 'EQUALS', 'NOT_EQ'),
    ('left', 'SMALLER', 'GREATER', 'SMALLER_EQ', 'GREATER_EQ'),
    ('nonassoc', 'LPAREN')
]

def p_ident_expr(p):
    'IDENTIFIER_EXPR : IDENTIFIER'
    p[0] = p[1]

def p_expression_ident(p):
    'expression : IDENTIFIER_EXPR'
    p[0] = ('var', p[1])

def p_expression_num(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_bool(p):
    'expression : BOOLEAN'
    p[0] = ('bool', p[1])

def p_expression_char(p):
    "expression : CHAR"
    p[0] = ('char', p[1])

def p_expression_string(p):
    "expression : STRING"
    p[0] = ('string', p[1])

def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = ('paren', p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression
           | expression AND_BIT expression
           | expression OR_BIT expression
           | expression MOD expression
           | expression XOR_BIT expression
           | expression SMALLER expression
           | expression GREATER expression
           | expression EQUALS expression
           | expression SMALLER_EQ expression
           | expression GREATER_EQ expression
           | expression NOT_EQ expression
           | expression AND_BOOL expression
           | expression OR_BOOL expression
           | expression XOR_BOOL expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_unop(p):
    '''expression : NOT_BIT expression
                  | NOT_BOOL expression
                  | MINUS expression'''
    p[0] = ('unop', p[1], p[2])

# Array expression rules
# Array Deklaration: type, ident, size, array
def p_array_decl_l(p):
    '''declaration : TYPE LBRACKET size RBRACKET HASH IDENTIFIER LASSIGN array
                   | TYPE LBRACKET size RBRACKET HASH IDENTIFIER'''
    if len(p)==7:
        p[0] = ('decl_var', 'array', p[1], p[6], p[3], None)
    else:
        p[0] = ('decl_var', 'array', p[1], p[6], p[3], p[8])

def p_array_decl_r(p):
    '''declaration : array RASSIGN IDENTIFIER HASH LBRACKET size RBRACKET TYPE
                   | IDENTIFIER HASH LBRACKET size RBRACKET TYPE'''
    
    if len(p)==7:
        p[0] = ('decl_var', 'array', p[6], p[1], p[4])
    else:
        p[0] = ('decl_var', 'array', p[8], p[3], p[6], p[1])

def p_array_size(p):
    '''size : INDEX
            | empty'''
    p[0] = p[1] if len(p) == 2 else None

def p_empty(p):
    'empty :'
    pass

def p_expr_array(p):
    'array : LBRACKET arg_list RBRACKET'
    p[0] = ('array', p[2])

def p_array_get(p):
    'expression : IDENTIFIER LBRACKET INDEX RBRACKET'
    p[0] = ('array_get', p[1], p[3])

# List expression rules
def p_list_type_l(p):
    '''list_type_l : LIST WITH TYPE'''
    p[0] = p[3]

def p_list_type_r(p):
    'list_type_r : TYPE WITH LIST'
    p[0] = p[1]

# Listen Deklaration: type, ident, liste
def p_list_decl_l(p):
    '''declaration : list_type_l HASH IDENTIFIER
                   | list_type_l HASH IDENTIFIER LASSIGN list'''
    if len(p)==4:
        p[0] = ('decl_var', 'list', p[1], p[3], None)
    else:
        p[0] = ('decl_var', 'list', p[1], p[3], p[5])

def p_list_decl_r(p):
    '''declaration : IDENTIFIER HASH list_type_r
                   | list RASSIGN IDENTIFIER HASH list_type_r'''
    if len(p)==4:
        p[0] = ('decl_var', 'list', p[3], p[1], None)
    else:
        p[0] = ('decl_var', 'list', p[5], p[3], p[1])

def p_expr_list(p):
    'list : LPAREN arg_list RPAREN'
    p[0] = ('list', p[2])

def p_list_get(p):
    'expression : IDENTIFIER DOT GET LPAREN INDEX RPAREN'
    p[0] = ('list_get', p[1], p[5])

# Argumente der Arrays und Listen
def p_arg_list(p):
    '''arg_list : expression COMMA arg_list
                | expression'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_lambda_exp(p):
    'expression : HASH WITH LPAREN param_list RPAREN FUNCARROW TYPE DO block DONE'
    p[0] = ('lambda', p[4], p[7], p[9])

def p_stm(p):
    '''statement : assign
                 | declaration
                 | condition
                 | iteration
                 | func_decl
                 | return
                 | ctn
                 | brk
                 | onbrk
                 | expression'''
    p[0] = p[1]

def p_block_single(p):
    'block : statement_list'
    p[0] = p[1]

def p_stmt_list_multi(p):
    'statement_list : statement_list statement SEMICOLON'
    p[0] = p[1] + [p[2]]

def p_stmt_list_single(p):
    'statement_list : statement SEMICOLON'
    p[0] = [p[1]]

def p_print_stm(p):
    'statement : PRINT LPAREN expression RPAREN'
    p[0] = ('print', p[3])

# Variablen Deklaration und Zuweisung
def p_assign_stm(p):
    '''assign : IDENTIFIER LASSIGN expression
              | expression RASSIGN IDENTIFIER'''
    if p[2] == '<-':
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = ('assign', p[3], p[1])

def p_decl_var_stm_l(p):
    '''declaration : TYPE HASH IDENTIFIER LASSIGN expression'''
    p[0] = ('decl_var', p[1], p[3], p[5])

def p_decl_var_stm_r(p):
    'declaration : expression RASSIGN IDENTIFIER HASH TYPE'
    p[0] = ('decl_var', p[5], p[3], p[1])

def p_decl_var_stm_empty_l(p):
    'declaration : TYPE HASH IDENTIFIER'
    p[0] = ('decl_var', p[1], p[3], None)

def p_decl_var_stm_empty_r(p):
    'declaration : IDENTIFIER HASH TYPE'
    p[0] = ('decl_var', p[3], p[1], None)

# Condition Parser im Format ('cond', condition, if_block, elif_list, else_block)
def p_cond_if(p):
    'condition : IF expression DO block DONE'
    p[0] = ('cond', p[2], p[4], [], None)

def p_cond_if_else(p):
    'condition : IF expression DO block ELSE DO block DONE'
    p[0] = ('cond', p[2], p[4], [], p[7])

def p_cond_if_elif(p):
    'condition : IF expression DO block elif_list DONE'
    p[0] = ('cond', p[2], p[4], p[5], None)

def p_cond_if_elif_else(p):
    'condition : IF expression DO block elif_list ELSE DO block DONE'
    p[0] = ('cond', p[2], p[4], p[5], p[8])

def p_elif(p):
    '''elif : ELIF expression DO block'''
    p[0] = (p[2], p[4])

def p_elif_list_single(p):
    'elif_list : elif'
    p[0] = [p[1]]

def p_elif_list_multi(p):
    'elif_list : elif_list elif'
    p[0] = p[1] + [p[2]]

#iteration
def p_iter_stm(p):
    'iteration : UNTIL expression DO block DONE'
    p[0] = ('iter', p[2], p[4])

def p_iter_do_stm(p):
    'iteration : DO block DONE UNTIL expression'
    p[0] = ('iter', p[5], p[2])

# Parser für Funktions Deklaration
def p_func_decl(p):
    '''func_decl : FUNC HASH IDENTIFIER LASSIGN WITH LPAREN param_list RPAREN FUNCARROW TYPE DO block DONE'''
    p[0] = ('func_decl', p[3], p[10], p[7], p[12])

def p_func_param_list(p):
    '''param_list : param_list COMMA param'''
    p[0] = p[1] + [p[3]]

def p_func_param_list_single(p):
    '''param_list : param'''
    p[0] = [p[1]]

def p_func_param(p):
    '''param : TYPE HASH IDENTIFIER'''
    p[0] = (p[1], p[3])

# Parser für Funktionsaufruf
def p_func_param_call_list_multi(p):
    'param_call_list : param_call_list COMMA expression'
    p[0] = p[1] + [p[3]]

def p_func_param_call_list_single(p):
    'param_call_list : expression'
    p[0] = [p[1]]

def p_func_call_empty(p):
    'expression : IDENTIFIER LPAREN RPAREN'
    p[0] = ('func_call', p[1], [])

def p_expression_func_call(p):
    'expression : IDENTIFIER LPAREN param_call_list RPAREN'
    p[0] = ('func_call', p[1], p[3])

# Return Parser Regel
def p_ret_stm(p):
    'return : RETURN expression'
    p[0] = ('return', p[2])

# Iterations Kontroll Regeln
def p_con_stm(p):
    'ctn : CONTINUE'
    p[0] = ['ctn']

def p_break_stm(p):
    'brk : BREAK'
    p[0] = ['brk']

def p_on_break_stm(p):
    'onbrk : ONBREAK statement'
    p[0] = ('onbrk', [p[2]])

# Programm Regel
def p_program_multiple(p):
    '''program : program statement SEMICOLON'''
    p[0] = p[1] + [p[2]]

def p_program_single(p):
    '''program : statement SEMICOLON'''
    p[0] = [p[1]]

# Error Funktion
def p_error(p):
       if p:
           print(f"Syntax error at line {p.lineno}, unexpected token {p.type} ('{p.value}')")
       else:
           print("Syntax error at EOF")

parser = yacc(start='program')