from pygame import Surface, SRCALPHA, Color, Rect, mouse, Vector2 as V2
from typing import Sequence, Any, TypeVar
from copy import deepcopy

from any.screen import screen

RGBAOutput = tuple[int, int, int, int]
ColorValue = Color | int | str | tuple[int, int, int] | RGBAOutput | Sequence[int]

def rect_fill(color: ColorValue, rect: Rect, surface: Surface=screen) -> None:
    source = Surface(size=rect.size, flags=SRCALPHA)
    source.fill(color=color)
    surface.blit(source=source, dest=rect)

def ratio_rect(rect: Rect, ratio: tuple[int | float, int | float] | V2) -> Rect:
    w, h = (ratio[0]*rect.h/ratio[1], rect.h) if rect.w*ratio[1] > rect.h*ratio[0] else (rect.w, ratio[1]*rect.w/ratio[0])
    return Rect(rect.left+(rect.w-w)/2, rect.top+(rect.h-h)/2, w, h)

def translucented_color(color: ColorValue, a: int=128) -> Color:
    ret = deepcopy(Color(color))
    ret.a = int(a)
    return ret

def cursor_in_rect(rect: Rect) -> bool:
    mx, my = mouse.get_pos()
    return rect.left <= mx and mx <= rect.right and rect.top <= my and my <= rect.bottom

T = TypeVar('T')

def enforce(__object: Any, __type: type[T]) -> T:
    if not isinstance(__object, __type):
        raise ValueError(f"{__object} is not an instance of {__type.__name__}")
    return __object

