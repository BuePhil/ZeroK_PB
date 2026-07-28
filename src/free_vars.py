def fv_exp(exp):
    match exp: 
        case ('var', name):
            return {name}
        case ('binop', op, lexp, rexp):
            return fv_exp(lexp) | fv_exp(rexp)
        case ('func_call', name, args):
            fvs = fv_exp(name)
            for arg in args: fvs |= fv_exp(arg)
            return fvs
        case ('lambda', args, ty, body):
            return fv_stm(body) - {name for name, ty in args}
        case _: return set()

def fv_stm(stms):
    if len(stms) == 0: return set()
    head, tail = stms[0], stms[1:]
    fv, bv = set(), set()

    match head:
        case ('decl_var', ty, name, exp):
            fv = fv_exp(exp); bv = {name}
        case ('print', body):
            fv = fv_exp(body)
        case _: fv = set()

    return fv | (fv_stm(tail) - bv)