from pygame import Color
from typing import Sequence

from mod.kard import Kard, EMPTY_KARD

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

class ManPlayer():
    def __init__(self, name: str, color: ColorValue, log: list[Kard]) -> None:
        self.name = name
        self.color = Color(color)
        self.hand = EMPTY_KARD
        self.log = log
        self.alive = True