from pygame import Surface
from typing import NamedTuple

from any.pictures import picload

class Kard(NamedTuple):
    name: str
    rank: int
    png_file: str

    def picture(self) -> Surface:
        return picload(self.png_file)
