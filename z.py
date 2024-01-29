class Coord:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

class Hoge:
    def __init__(self, text: str, coord: Coord) -> None:
        self.text, self.coord = text, coord

h1 = Hoge()
print(h1)

h1.coord.x, h1.coord.y = 15, 40
print(h1)

h2 = Hoge()
print(h2)