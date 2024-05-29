
# from typing import NamedTuple

# class Gewo(NamedTuple):
#     x: int
#     y: int

# class Hoge(NamedTuple):
#     gewos: list[Gewo]

# hhh = Hoge([Gewo(0, 1), Gewo(1, 2), Gewo(3, 5), Gewo(8, 13), Gewo(21, 34)])

# print(hhh)
# hhh._replace(
#     gewos=[Gewo(1, 1), Gewo(4, 2), Gewo(9, 3), Gewo(16, 4), Gewo(25, 5)]
# )
# print(hhh)
# hhh.gewos[2]._replace(
#     x=99,
#     y=99
# )
# print(hhh)

# li = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
# z = "Zehta"
# idx = li.index(z)
# print(li.index("Gamma"), li.index(z))

n = 3
li = list(range(4))
cu = li[n:]+li[:n]
print(li, cu)