from dataclasses import dataclass
from typing import runtime_checkable, Protocol

@runtime_checkable
class Printable(Protocol):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        ...

    def print(self) -> None:
        ...

@dataclass
class ClsA:
    x: int
    y: int

    def print(self) -> None:
        print(f"座標は({self.x}, {self.y})です")

@dataclass
class ClsB:
    x: int
    y: int

    def print(self) -> None:
        print(f"和は({self.x+self.y}、差は {self.x-self.y})です")

li: list[tuple[type[Printable], int, int]] = [(ClsA, 10, 20), (ClsB, 30, 40)]

for cls, x, y in li:
    cls(x, y).print()