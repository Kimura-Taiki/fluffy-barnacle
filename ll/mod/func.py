from pygame import Surface, SRCALPHA, Color, Rect
from typing import Callable, Any, Sequence

from mod.screen import screen

def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(f"{text} が未注入です")
    return raise_func

def pass_func() -> None:
    ...

def mono_func(any: Any) -> None:
    ...

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

def rect_fill(color: ColorValue, rect: Rect, surface: Surface=screen) -> None:
    source = Surface(size=rect.size, flags=SRCALPHA)
    source.fill(color=color)
    surface.blit(source=source, dest=rect)
