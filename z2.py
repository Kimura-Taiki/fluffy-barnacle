from typing import Protocol, runtime_checkable

@runtime_checkable
class Mozi(Protocol):
    def mes(self) -> None:
        ...

class Alpha():
    def __init__(self) -> None:
        pass

    def mes(self) -> None:
        print("Alphaです")

class Beta():
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def mes(self) -> None:
        print(f"Beta({self.x}, {self.y})です")

class Gamma():
    def __init__(self, s: str) -> None:
        self.s = s

    def mes(self) -> None:
        print(f"Gamma({self.s}, {len(self.s)}文字)です")

if not isinstance(Alpha(), Mozi):
    raise ValueError

Mozi.register(Alpha)

a = Alpha()
b = Beta(10, 20)
c = Gamma("Hoge")
li: list[Mozi] = [a, b, c]
for mozi in li:
    mozi.mes()