from pygame import Surface, SRCALPHA, Color, Rect
from typing import Callable, Any

from mod.screen import screen

def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(f"{text} が未注入です")
    return raise_func

def pass_func() -> None:
    ...

def mono_func(any: Any) -> None:
    ...

def rect_fill(color: Any, rect: Rect) -> None:
    source = Surface(size=rect.size, flags=SRCALPHA)
    source.fill(color=color)
    screen.blit(source=source, dest=rect)