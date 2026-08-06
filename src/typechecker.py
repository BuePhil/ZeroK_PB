import sys

sys.path.insert(0, "../classes")

from environment import *
from Types import *
from ReturnSignal import ReturnSignal
from iter_control import *
from free_vars import *

unops = {
    '-' : ('int' , 'int'),
    '!!': ('bool', 'bool'),
    '!' : ('int' , 'int'),
}


binops = {
    #       opt 1                   opt 2
    '+' : (                        # + hat mehrere Regeln, da es auch für die konkaternierung mit Strings funktioniert
    (('int', 'int'), 'int'),       # TODO: für Listen und Arrays diese konkatenierung hinzufügen
    (('string', 'string'), 'string'),
    (('int', 'string'), 'string'),
    (('string', 'int'), 'string'),
    (('string', 'bool'), 'string'),
    (('bool', 'string'), 'string')
    ),
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

def typecheck(prog):
    env = make_ev_env()

    ty_stms(prog, env)

def ty_expr(node, env):

    if isinstance(node, int):
        return 'int'

    match node:
        case ('num', (n, b, t)):
            return 'int'
        case ('bool', b):
            return 'bool'
        case ('string', s):
            return 'string'
        case ('var', name):
            ty = env.lookup(name).ty
            if (isinstance(ty, tuple)           # Überprüfung in dem Format, da variablen mit Arrays
                and len(ty) == 2                # oder Listen als Werten auch Tupel als Typenhabe
                and isinstance(ty[0], tuple)
            ):
                raise TypeError(f"'{name}' ist eine Funktion und kein Wert")
            return ty
        case ('paren', expr):
            return ty_expr(expr, env)
        case ('unop', op, expr):
            ty_in, ty_out = unops[op]
            got = ty_expr(expr, env)
            if got != ty_in:
                raise TypeError(f"unop '{op}' erwartet {ty_in}, bekam {got}")
            return ty_out
        case ('binop', op, lexp, rexp):
            l_ty = ty_expr(lexp, env)
            r_ty = ty_expr(rexp, env)
            for (ty_in, ty_out) in binops[op]:
                if ty_in == (l_ty, r_ty):
                    return ty_out
            raise TypeError(f"binop '{op}' nicht definiert fuer ({l_ty}, {r_ty})")
        case ('func_call', name, args):
            return check_func_call(name, args, env)
        case ('lambda', args, ty, body):
            return check_lambda(args, ty, body, env)

        case ('array', values):     # Vereinfachung zum Typchecken von Arrays
            if not values:
                return ('array', None, 0)

            elem_ty = ty_expr(values[0], env)

            for val in values[1:]:
                ty = ty_expr(val, env)
                if ty != elem_ty:
                    raise TypeError(f"Array enthaelt verschiedene Typen ({elem_ty}, {ty})")

            return ('array', elem_ty, len(values))

        case ('list', values):     # Vereinfachung zum Typchecken von Listen
            if not values:
                return ('list', None)

            elem_ty = ty_expr(values[0], env)
            for val in values[1:]:
                ty = ty_expr(val, env)
                if ty != elem_ty:
                    raise TypeError(f"Liste enthaelt verschiedene Typen ({elem_ty}, {ty})")

            return ('list', elem_ty)

        case ('array_get', name, index):
            arr_ty = env.lookup(name).ty

            if not isinstance(arr_ty, tuple) or arr_ty[0] != 'array':
                raise TypeError(f"'{name}' ist kein Array")

            if ty_expr(index, env) != 'int':
                raise TypeError("Arrayindex muss int sein")

            return arr_ty[1]

        case ('list_get', name, index):
            lst_ty = env.lookup(name).ty

            if not isinstance(lst_ty, tuple) or lst_ty[0] != 'list':
                raise TypeError(f"'{name}' ist keine Liste")

            if ty_expr(index, env) != 'int':
                raise TypeError("Listenindex muss int sein")

            return lst_ty[1]
        case _:
            raise SyntaxError(f"Unbekannter Ausdruck: {node}")

def check_lambda(args, ty_ret, body, env):
    # nur die freien Variablen aus der Umgebung uebernehmen, analog zum Interpreter
    env_ = Env()
    for name in fv_exp(('lambda', args, ty_ret, body)):
        entry = env.lookup(name)
        env_.put(name).ty = entry.ty
    for (pty, pname) in args:
        env_.put(pname).ty = pty
    ty_stms(body, env_, ret_ty=ty_ret)
    ty_args = tuple(pty for pty, _ in args)
    return (ty_args, ty_ret)

def ty_stms(node, env, ret_ty=None):
    
    for arg in node:
        match arg[0]:
            case 'decl_var':
                check_decl_var(arg[1:], env)
            case 'print':
                ty_expr(arg[1], env)
            case 'assign':
                check_assign(arg[1:], env)
            case 'cond':
                check_cond(arg[1:], env, ret_ty)
            case 'iter':
                check_iter(arg[1:], env, ret_ty)
            case 'func_decl':
                check_func_decl(arg[1:], env)
            case 'func_call':
                ty_expr(arg, env)
            case 'return':
                check_return(arg[1], env, ret_ty)
            case 'ctn' | 'brk':
                pass
            case 'onbrk':
                ty_stms(arg[1], env, ret_ty)
            case _:
                raise SyntaxError(f"Unbekanntes Statement: {arg}")

def check_decl_var(node, env):
    ty_var = node[0]

    if ty_var=='array':
        _, elem_ty, name, size, arr = node

        env.put(name).ty = ('array', elem_ty, size)

        if arr is not None:
            ty = ty_expr(arr, env)
            if ty[0] != 'array':
                raise TypeError("Initialisierung ist kein Array")
            if ty[1] != elem_ty:
                raise TypeError(f"Array '{name}' erwartet Elemente vom Typ {elem_ty}")
            if size is not None and ty[2] != size:
                print(repr(size), type(size))
                print(repr(ty[2]), type(ty[2]))
                print("equal?", ty[2] == size)
                raise TypeError(f"Array '{name}' erwartet Groesse {size}")
        return

    if ty_var=='list':
        _, elem_ty, name, lst = node

        env.put(name).ty = ('list', elem_ty)

        if lst is not None:
            ty = ty_expr(lst, env)

            if ty[0] != 'list':
                raise TypeError("Initialisierung ist keine Liste")
            if ty[1] != elem_ty:
                raise TypeError(f"Liste '{name}' erwartet Elemente vom Typ {elem_ty}")
        return

    ty_lhs, name, exp = node

    if exp is not None:
        ty_rhs = ty_expr(exp, env)
        if ty_lhs != ty_rhs:
            raise TypeError(f"Deklaration von '{name}': erwartet {ty_lhs}, bekam {ty_rhs}")
    env.put(name).ty = ty_lhs

def check_assign(node, env):
    name, exp = node
    ty_lhs = env.lookup(name).ty
    ty_rhs = ty_expr(exp, env)
    if ty_lhs != ty_rhs:
        raise TypeError(f"Zuweisung an '{name}': erwartet {ty_lhs}, bekam {ty_rhs}")

def check_cond(node, env, ret_ty):
    cond, then_body, elifs, else_body = node

    if ty_expr(cond, env) != 'bool':
        raise TypeError("Bedingung von 'if' muss vom Typ bool sein")
        
    ty_stms(then_body, env.push(), ret_ty)

    for (el_cond, el_body) in elifs:
        if ty_expr(el_cond, env) != 'bool':
            raise TypeError("Bedingung von 'elif' muss vom Typ bool sein")
        ty_stms(el_body, env.push(), ret_ty)

    if else_body is not None:
        ty_stms(else_body, env.push(), ret_ty)

def check_iter(node, env, ret_ty):
    cond, body = node
    if ty_expr(cond, env) != 'bool':
        raise TypeError("Bedingung der Schleife muss vom Typ bool sein")
    ty_stms(body, env.push(), ret_ty)

def check_func_decl(node, env):
    name, ty_ret, params, body = node

    if env.exist_func(name):
        raise TypeError(f"Funktion '{name}' bereits deklariert")

    ty_args = tuple(ty for ty, n_arg in params)
    env.put(name).ty = (ty_args, ty_ret)
    env_ = env.push()

    for (pty, pname) in params:
        env_.put(pname).ty = pty

    ty_stms(body, env_, ret_ty=ty_ret)

def check_func_call(name, args, env):
    entry = env.lookup(name)

    if not (isinstance(entry.ty, tuple) and len(entry.ty) == 2):
        raise TypeError(f"'{name}' ist keine Funktion")

    ty_args, ty_ret = entry.ty

    if len(args) != len(ty_args):
        raise TypeError(f"'{name}' erwartet {len(ty_args)} Argument(e), bekam {len(args)}")

    for expected, arg in zip(ty_args, args):
        got = ty_expr(arg, env)

        if got != expected:
            raise TypeError(f"'{name}': Argument vom Typ {expected} erwartet, bekam {got}")

    return ty_ret

def check_return(exp, env, ret_ty):
    if ret_ty is None:
        raise TypeError("'return' ausserhalb einer Funktion")
    ty_val = ty_expr(exp, env)
    if ty_val != ret_ty:
        raise TypeError(f"'return': erwartet {ret_ty}, bekam {ty_val}")