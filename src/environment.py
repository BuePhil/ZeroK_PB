from dataclasses import dataclass
from typing import Any

class Env:
    # Eine Liste die ein Parent und ein Dictionary hat.
    # das Dictionary enthält alle, im Scope existierenden
    # Variablen und deren Werte.

    __slots__ = ('parent', 'refs')

    def __init__(self, parent=None):
        self.parent = parent
        self.refs = {}

    def put(self, name):
        self.refs[name] = EnvEntry(name, None, None)
        return self.refs[name]

    def assign_var(self, ident, val):
        self.lookup(ident).value = val

    def assign_fun(self, name, args, stms):
        self.lookup(name).value = Closure(args, stms, self)

    def push(self):
        return Env(self)

    def value(self, name):
        return self.lookup(name).value

    def lookup(self, name):
        env = self

        while env is not None:
            if name in env.refs:
                return env.refs[name]

            env = env.parent
    
        raise NameError(f"Reference with name {name} doesn't exist")
    
    def exist_func(self, name):
        try:
            self.lookup(name)
            return True
        except NameError:
            return False

@dataclass
class FuncType:
    ty_args: Any
    ty_ret: type

@dataclass
class EnvEntry:
    ident: str
    ty: type | FuncType
    value: Any | None

@dataclass
class Closure:
    args: Any
    body: Any
    env: Env