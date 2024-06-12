from pygame import Surface, Color
from pygame.font import Font
from typing import Callable, Sequence

from any.locales import lomes

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

LL_RENDER: Callable[[str, int, ColorValue], Surface] = lambda s, i, c: Font(
    f"ll/font/{lomes(folder="board", key="font")}", i
).render(s, True, c)