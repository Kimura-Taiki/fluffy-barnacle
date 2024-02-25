from copy import copy, deepcopy

class Hoge:
    def __init__(self, text: str="") -> None:
        self.text = text

class Coord:
    def __init__(self, x, y) -> None:
        self.x, self.y, self.hoge = x, y, Hoge()

    # def __eq__(self, other):
    #     if isinstance(other, Coord):
    #         return self.x == other.x and self.y == other.y
    #     return False

a = Coord(100, 200)
b = a
c = copy(a)
d = deepcopy(a)
e = Coord(100, 200)

print("A", a!=a, a is not a)
print("B", a!=b, a is not b)
print("C", a!=c, a is not c)
print("D", a!=d, a is not d)
print("E", a!=e, a is not e)
