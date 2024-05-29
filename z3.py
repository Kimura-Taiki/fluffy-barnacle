from dataclasses import dataclass

@dataclass
class Hoge():
    li: list[int]

hhh = Hoge([0, 1, 2, 0])
print(hhh)