#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, BRIGHT
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller
from mod.delivery import Delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 600/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-144

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 0

def kirihuda_made_by_files(surfaces: list[Surface], delivery: Delivery, is_own: bool) -> Taba:
    tehuda = Taba(delivery=delivery, is_own=is_own, inject=_inject_of_tehuda)
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

def _inject_of_tehuda(huda: Huda, taba: Taba) -> None:
    huda.inject_funcs(draw=_draw, hover=Huda.detail_draw)

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    elif controller.hover == huda:
        pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
        screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
    else:
        default_draw(huda=huda)
    return None
