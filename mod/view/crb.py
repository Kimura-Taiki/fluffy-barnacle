from pygame import Surface, mouse, Rect, image, transform, Vector2 as V2, SRCALPHA
from pygame.font import Font
from typing import Callable, Any
from functools import partial

from mod.const.screen import screen
from mod.const.func import rect_fill

def _hoge(any: Any) -> None:
    ...

def _text() -> str:
    return "hoge"

MS_MINCHO_COL: Callable[[str, int, tuple[int, int, int]], Surface] = lambda s, i, c: Font("msmincho001.ttf", i).render(s, True, c)

_img_frame = image.load("pictures/ww_bo.png").convert_alpha()
_part_size = V2(_img_frame.get_size())/3
_px, _py = _part_size.x, _part_size.y
def _part(i: int) -> Surface:
    img = Surface(_part_size, SRCALPHA)
    img.blit(source=_img_frame, dest=Rect(0, 0, _px, _py), area=Rect(i%3*_px, i//3*_py, _px, _py))
    return img
_img_parts = [_part(i) for i in range(9)]

class Crb():
    def __init__(self, img: Surface, rect: Rect, scale: float,
    text_func: Callable[[], str]=_text,
    draw: Callable[['Crb'], None]=_hoge, hover: Callable[['Crb'], None]=_hoge,
    mousedown: Callable[['Crb'], None]=_hoge, active: Callable[['Crb'], None]=_hoge,
    mouseup: Callable[['Crb'], None]=_hoge, drag: Callable[['Crb'], None]=_hoge,
    dragend: Callable[['Crb'], None]=_hoge) -> None:
        self.rect = rect
        self.scale = scale
        # self.draw: Callable[[], None] = partial(draw, self)
        self.draw = self._draw
        self.hover: Callable[[], None] = partial(hover, self)
        self.mousedown: Callable[[], None] = partial(mousedown, self)
        self.active: Callable[[], None] = partial(active, self)
        self.mouseup: Callable[[], None] = partial(mouseup, self)
        self.drag: Callable[[], None] = partial(drag, self)
        self.dragend: Callable[[], None] = partial(dragend, self)

    def is_cursor_on(self) -> bool:
        mx, my = mouse.get_pos()
        r = self.rect
        return r.left <= mx and mx <= r.right and r.top <= my and my <= r.bottom

    def _draw(self) -> None:
        rect_fill((0, 255, 0, 128), self.rect)
        params = [(_img_parts[0], _part_size, V2(self.rect.topleft)),
                  (_img_parts[1], V2(self.rect.w-_px*2, _py), V2(self.rect.topleft)+(_px, 0)),
                  (_img_parts[2], _part_size, V2(self.rect.topright)-(_px, 0)),
                  (_img_parts[3], V2(_px, self.rect.h-_py*2), V2(self.rect.topleft)+(0, _py)),
                  (_img_parts[4], V2(self.rect.w-_px*2, self.rect.h-_py*2), V2(self.rect.topleft)+(_px, _py)),
                  (_img_parts[5], V2(_px, self.rect.h-_py*2), V2(self.rect.topright)+(-_px, _py)),
                  (_img_parts[6], _part_size, V2(self.rect.bottomleft)-(0, _py)),
                  (_img_parts[7], V2(self.rect.w-_px*2, _py), V2(self.rect.bottomleft)+(_px, -_py)),
                  (_img_parts[8], _part_size, V2(self.rect.bottomright)-_part_size),
                  ]
        for img, size, dest in params:
            screen.blit(source=transform.scale(surface=img, size=size), dest=dest)
        
