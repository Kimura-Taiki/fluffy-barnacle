from pygame import Color

from typing import Sequence

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

class ManPlayer():
    def __init__(self, name: str, color: ColorValue) -> None:
        self.name = name
        self.color = Color(color)