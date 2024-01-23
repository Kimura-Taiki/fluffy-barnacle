#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.math import Vector2
from typing import Callable
from functools import partial, partialmethod

from mod.const import WX, WY, screen, BRIGHT, IMG_BACK
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller
from mod.delivery import Delivery

HAND_X: Callable[[int, int], int | float] = lambda i, j: 340+286/2

HAND_Y_DIFF: Callable[[int], float] = lambda i: -36 if i < 4 else -144/i
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-102+HAND_Y_DIFF(j)*i

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 90.0

def husehuda_made_by_files(surfaces: list[Surface], delivery: Delivery, is_own: bool) -> Taba:
    husehuda = Taba(delivery=delivery, is_own=is_own, inject=_inject_of_husehuda)
    husehuda.var_rearrange = partial(_rearrange_husehuda, taba=husehuda)
    for i in surfaces:
        husehuda.append(Huda(img=i))
    return husehuda

def _rearrange_husehuda(taba: Taba) -> None:
    angle_func, x_func, y_func = _rearrange_funcs(l=len(taba), is_own=taba.is_own)
    [huda.rearrange(angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i)) for i, huda in enumerate(taba)]

def _rearrange_funcs(l: int, is_own: bool) -> tuple[Callable[[int], float], Callable[[int], float], Callable[[int], float]]:
    if is_own:
        return partial(HAND_ANGLE, j=l), partial(HAND_X, j=l), partial(HAND_Y, j=l)
    else:
        return (partial(lambda i, j: HAND_ANGLE(i, j)+180.0, j=l),
                partial(lambda i, j: WX-HAND_X(i, j), j=l), partial(lambda i, j: WY-HAND_Y(i, j), j=l))

def _inject_of_husehuda(huda: Huda, taba: Taba) -> None:
    huda.inject_funcs(draw=_draw, hover=_hover)
    
def _draw(huda: Huda) -> None:
    _husehuda_draw(huda=huda)
    return None

def _husehuda_draw(huda: Huda) -> None:
    for i in range(19):
        IMG_BACK.set_alpha(i*25+30)
        screen.blit(source=IMG_BACK, dest=huda.img_rz_topleft+[0, i*20], area=(0, i*20, 285, 20))
    IMG_BACK.set_alpha(255)
    screen.blit(source=IMG_BACK, dest=huda.img_rz_topleft+[0, 180], area=(0, 180, 285, 24))
    for i in range(4):
        huda.img_rz.set_alpha(i*48+48)
        screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, i*9+132], area=(0, i*9+132, 285, 9))
    huda.img_rz.set_alpha(224)
    screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, 168], area=(0, 168, 285, 36))
    huda.img_rz.set_alpha(255)

def _hover(huda: Huda) -> None:
    screen.blit(source=huda.img_nega, dest=[WX-huda.img_nega.get_width(), 0])
