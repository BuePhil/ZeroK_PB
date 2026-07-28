from environment import Env
from IceInt import IceInt
from ReturnSignal import ReturnSignal

unops = {
    '-' : ('int' , 'int'),
    '!!': ('bool', 'bool'),
    '!' : ('int' , 'int'),
}


binops = {
    #       opt 1                   opt 2
    '+' : ( (('int', 'int'), 'int') , ),
    '-' : ( (('int', 'int'), 'int') , ),
    '*' : ( (('int', 'int'), 'int') , ),
    '/' : ( (('int', 'int'), 'int') , ),
    '%' : ( (('int', 'int'), 'int') , ),
    '&' : ( (('int', 'int'), 'int') , ),
    '|' : ( (('int', 'int'), 'int') , ),
    '^' : ( (('int', 'int'), 'int') , ),
    '<' : ( (('int', 'int'), 'bool'), ),
    '>' : ( (('int', 'int'), 'bool'), ),
    '=' : ( (('int', 'int'), 'bool'), ),
    '<=' : ( (('int', 'int'), 'bool'), ),
    '>=' : ( (('int', 'int'), 'bool'), ),
    '!=' : ( (('int', 'int'), 'bool'), (('bool', 'bool'), 'bool')),
    '&&' : ( (('bool', 'bool'), 'bool'), ),
    '||' : ( (('bool', 'bool'), 'bool'), ),
    '^^' : ( (('bool', 'bool'), 'bool'), ),
}

def ty_expr(node):
    match node:
        case ('num', n, b, t): return 'int'
        case ('bool', b): return 'bool'
        case ('paren', expr): return ty_expr(expr)

        case ('unop', op, expr):
            # input and output type
            (i, o) = unops[op]
            if (ty_in := ty_expr(expr)) == i:
                return o
            else: raise TypeError('unop', op, i, ty_in)
        case ('binop', op, lexp, rexp):
            in_out = binops[op]
            ty_ins = tuple([ty_expr(x) for x in [lexp,rexp]])

            for (i, o) in in_out:
                if i == ty_ins: return o
            
            raise TypeError
        case _: raise SyntaxError
