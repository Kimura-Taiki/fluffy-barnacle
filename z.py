from typing import Any
from mod.const import enforce

class Hoge():
    def __init__(self, name: str) -> None:
        self.name = name

a = Hoge("Alpha")
b = Hoge("Beta")
c = Hoge("Gamma")
d = Hoge("Delta")
li: list[Any] = [a, b, c, d]
print(li)
ef = [enforce(i, Hoge) for i in li]
print(ef)