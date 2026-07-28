from dataclasses import dataclass

@dataclass
class IceInt:
    value: int
    base: int
    ty: str

    def __repr__(self):
        return(f'{self.value}')