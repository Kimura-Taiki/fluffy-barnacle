from dataclasses import dataclass, field

@dataclass
class Hoge():
    name: str
    reserve: list[int] = field(default_factory=lambda: [1, 2, 3])

h1 = Hoge("Alpha")
h2 = Hoge("Beta")
print(h1, h2)
h1.reserve.append(4)
print(h1, h2)
