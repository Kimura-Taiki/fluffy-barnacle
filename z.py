from typing import Protocol, runtime_checkable

@runtime_checkable
class Myp(Protocol):
    data: int

    def func(self) -> None:
        ...

class Hoge():
    data: int

    def __init__(self, data: int=0) -> None:
        self.data = data

    def func(self) -> None:
        print(f"data={self.data}")

print(type(Hoge), type(Myp))

print(isinstance(Hoge, Myp))
h = Hoge()
print(isinstance(h, Myp))