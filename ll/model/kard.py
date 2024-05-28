from pygame import Surface, image
from typing import NamedTuple

class Kard(NamedTuple):
    name: str
    png_file: str

    def picture(self) -> Surface:
        return image.load(self.png_file).convert_alpha()

EMPTY_KARD = Kard(name="empty", png_file="")