import sys

sys.path.insert(0, "./classes")

from ice_parser import parser
import typechecker as tc
from environment import *
from dataclasses import dataclass
from Types import *
from ReturnSignal import ReturnSignal
from iter_control import *
from free_vars import *

binops = {
    '+': lambda x, y: IceInt(x.value + y.value, x.base, x.ty),
    '-': lambda x, y: IceInt(x.value - y.value, x.base, x.ty),
    '*': lambda x, y: IceInt(x.value * y.value, x.base, x.ty),
    '/' : lambda x,y : IceInt(x.value / y.value, x.base, x.ty),
    '&' : lambda x,y : IceInt(x.value & y.value, x.base, x.ty),
    '|' : lambda x,y : IceInt(x.value | y.value, x.base, x.ty),
    '%' : lambda x,y : IceInt(x.value % y.value, x.base, x.ty),
    '^' : lambda x,y : IceInt(x.value ^ y.value, x.base, x.ty),
    '<' : lambda x,y : x.value < y.value,
    '>' : lambda x,y : x.value > y.value,
    '=' : lambda x,y : x.value == y.value,
    '<=': lambda x,y : x.value <= y.value,
    '>=': lambda x,y : x.value >= y.value,
    '!=': lambda x,y : x.value != y.value if(isinstance(x, IceInt)) else x != y,
    '&&': lambda x,y : x and y,
    '||': lambda x,y : x | y,
    '^^': lambda x,y : x ^ y
}

unops = {
    '!'  : lambda x : ~x.value, # Usage of Pythons itegrated bitwise not operator
    '!!' : lambda x : not x,
    '-'  : lambda x : -x.value
}

# Main function for correct interpreting of parenthesises, operators and types
def interpret(prog):
    env = make_ev_env()

    ev_stms(prog, env)

# Evaluation von Aussagen, die im Parser definiert wurden
def ev_exp(ast, env):

    if isinstance(ast, IceInt):
        return ast

    if isinstance(ast, IceArray):
        return ast

    if isinstance(ast, IceList):
        return ast

    if isinstance(ast, bool):
        return ast

    if isinstance(ast, str):
        return ast

    match ast:
        case ('var', name):
            return ev_exp(env.value(name), env)
        case ('num', (n, b, t)): return IceInt(int(n,b), b, t)
        case ('bool', b): return bool(b)
        case ('string', s): return s
        case ('paren', expr): return ev_exp(expr, env)
        case ('unop', op, expr): return unops[op](ev_exp(expr, env))
        case ('binop', op, lexp, rexp):
            left = ev_exp(lexp, env)
            right = ev_exp(rexp, env)
            
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)

            return binops[op](left, right)
        case ('func_call', name, args):
            closure = env.value(name)
            return ev_func_call(closure, args, env)
        case ('lambda', args, ty, body):
            env_ = Env()

            for name in fv_exp(ast):
                entry = env.lookup(name)

                new = env_.put(name)
                new.ty = entry.ty
                new.value = entry.value

            return Closure(args, body, env_)
        case ('array_get', name, index):
            val = env.value(name)

            if isinstance(val, IceArray):
                return val.value[index]
        case ('list_get', name, index):
            val = env.value(name)

            if isinstance(val, IceList):
                return val.value[index]
        case _: raise SyntaxError

# Evaluierung der im Parser definierten Statements
def ev_stms(ast, env):
    
    for arg in ast:
        match arg[0]:
            case 'decl_var':
                ev_decl(arg[1:], env)
            case 'print':
                print(f'> {ev_exp(arg[1], env)}')
            case 'assign':
                ev_assign(arg[1:], env)
            case 'cond':
                ev_cond(arg[1:], env)
            case 'iter':
                ev_iter(arg[1:], env)
            case 'func_decl':
                ev_func_decl(arg[1:], env)
            case 'func_call':
                ev_exp(arg, env)
            case 'return':
                value = ev_exp(arg[1], env)
                raise ReturnSignal(value)
            case 'ctn':
                raise ContinueSignal(arg[0])
            case 'brk':
                raise BreakSignal(arg[0])
            case'onbrk':
                raise OnBreakSignal(arg[1])
        pass

def ev_assign(arg, env):
    value = ev_exp(arg[1], env)
    env.assign_var(arg[0], value)

# Evaluierung der Deklaration
def ev_decl(decl, env):
    var_ty = decl[0]

    if var_ty=='array':
        var_ty = decl[1]
        arr = decl[4]
        if arr is not None:
            arr = [ev_exp(elem, env) for elem in arr[1]]
        env.put(decl[2]).ty = ('array', var_ty, decl[3])
        env.assign_var(decl[2], IceArray(decl[3], arr, var_ty))
    elif var_ty=='list':
        var_ty = decl[1]
        lst = decl[3]
        if lst is not None:
            lst = [ev_exp(elem, env) for elem in lst[1]]
        env.put(decl[2]).ty = ('list', var_ty)
        env.assign_var(decl[2], IceList(lst, var_ty))
    else:
        env.put(decl[1]).ty = decl[0]

        val = decl[2]    
        
        if val is not None:
            if(val[0] == 'lambda'):
                val = ev_exp(val, env)
            
            env.assign_var(decl[1], val)
    pass

def ev_cond(ast, env):
    # in cond wird nicht zu beginn _env erstellt, sondern ausgesondert für jeden Block
    if ev_exp(ast[0], env):
        ev_stms(ast[1], env.push())
    else:
        if not ast[2]: # elif Liste ist leer >> else block wird ausgeführt
            if not (ast[3] is None): # else Fall existiert
                ev_stms(ast[3], env.push())
        else:
            for el in ast[2]:
                if ev_exp(el[0], env):
                    ev_stms(el[1], env.push())
                    break
    pass

def ev_func_decl(node, env):
    name = node[0]

    if not(env.exist_func(name)):
        
        ty_args = tuple(ty for ty, n_arg in node[2])

        env.put(name).ty = (ty_args, node[1])
        env.assign_fun(name, node[2], node[3])
    else:
        print(f'Function {node[0]} already exists')
    pass

def ev_func_call(closure, args, env):

    call_env = closure.env.push()
    for (ty, name), arg in zip(closure.args, args):
        call_env.put(name).ty = ty
        call_env.assign_var(name, ev_exp(arg, env))

    try:
        ev_stms(closure.body, call_env)
        return None  # kein return im function body
    except ReturnSignal as r:
        return r.value
        
    pass

def ev_iter(ast, env):
    _env = env.push()

    while(not(ev_exp(ast[0], _env))):
        try:
            ev_stms(ast[1], _env)
        except ContinueSignal as c:
            continue
        except BreakSignal as b:
            break
        except OnBreakSignal as ob:
            ev_stms(ob.value, _env)
            break