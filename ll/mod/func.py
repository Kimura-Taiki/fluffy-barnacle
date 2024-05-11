from pygame import Color, Rect

from typing import Callable, Any

def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(f"{text} が未注入です")
    return raise_func

def pass_func() -> None:
    ...

def mono_func(any: Any) -> None:
    ...

def rect_fill(color: Any, rect: Rect) -> None:
    from pygame import Surface, SRCALPHA
    from mod.const.screen import screen
    source = Surface(size=rect.size, flags=SRCALPHA)
    source.fill(color=color)
    screen.blit(source=source, dest=rect)