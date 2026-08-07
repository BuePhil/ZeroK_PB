from dataclasses import dataclass
from typing import Any

@dataclass
class IceInt:
    value: int
    base: int
    ty: str

    def __repr__(self):
        return(f'{self.value}')

@dataclass
class IceArray:
    size: int
    value : Any
    ty: str

    def __repr__(self):
        return(f'{self.value}')

@dataclass
class IceList:
    value : Any
    ty: str

    def __repr__(self):
        return(f'{self.value}')