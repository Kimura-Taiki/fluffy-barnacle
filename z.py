from typing import NamedTuple

class Color(NamedTuple):
    r:int = 255
    g:int = 255
    b:int = 255

    def pos(self) -> None:
        print(f"({self.r}, {self.g}, {self.b})")

c = Color()
c.pos()