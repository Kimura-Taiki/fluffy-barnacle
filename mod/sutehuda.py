#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, BLACK
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.delivery import Delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 80-80*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2+70-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0.0

def sutehuda_made_by_files(surfaces: list[Surface], delivery: Delivery, is_own: bool) -> Taba:
    tehuda = Taba(delivery=delivery, is_own=is_own, inject=_inject_of_sutehuda)
    tehuda.var_rearrange = partial(_rearrange_tehuda, taba=tehuda)
    for i in surfaces:
        tehuda.append(Huda(img=i))
    return tehuda

def _rearrange_tehuda(taba: Taba) -> None:
    angle_func, x_func, y_func = _rearrange_funcs(l=len(taba), is_own=taba.is_own)
    [huda.rearrange(angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i)) for i, huda in enumerate(taba)]

def _rearrange_funcs(l: int, is_own: bool) -> tuple[Callable[[int], float], Callable[[int], float], Callable[[int], float]]:
    if is_own:
        return partial(HAND_ANGLE, j=l), partial(HAND_X, j=l), partial(HAND_Y, j=l)
    else:
        return (partial(lambda i, j: HAND_ANGLE(i, j)+180.0, j=l),
                partial(lambda i, j: WX-HAND_X(i, j), j=l), partial(lambda i, j: WY-HAND_Y(i, j), j=l))

def _inject_of_sutehuda(huda: Huda, taba: Taba) -> None:
    huda.inject_funcs(draw=_draw, hover=Huda.detail_draw)

def _draw(huda: Huda) -> None:
    pygame.draw.polygon(surface=screen, color=BLACK, points=huda.vertices, width=0)
    huda.img_rz.set_alpha(192)
    default_draw(huda=huda)
    huda.img_rz.set_alpha(255)
