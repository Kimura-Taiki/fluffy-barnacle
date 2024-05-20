from pygame import Surface, Color
from pygame.font import Font

from typing import Callable, Sequence

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

MS_MINCHO_COL: Callable[[str, int, ColorValue], Surface] = lambda s, i, c: Font("msmincho001.ttf", i).render(s, True, c)
