from pygame import Color
from typing import Sequence

from mod.kard import Kard

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

class ManPlayer():
    def __init__(self, name: str, color: ColorValue, log: list[Kard]) -> None:
        self.name = name
        self.color = Color(color)
        self.log = log