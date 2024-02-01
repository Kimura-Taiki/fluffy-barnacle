# from mod.req.req_send_huda import ReqSendHuda

from typing import NamedTuple
class Coord(NamedTuple):
    x:int = 0
    y:int = 0

    def length(self) -> float:
        return (self.x**2+self.y**2)**0.5

c1 = Coord(3, 4)
c2 = Coord(5, 12)
print(c1, c2)
print(c1.length(), c2.length())