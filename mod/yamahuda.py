#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, BRIGHT, IMG_YAMAHUDA
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller
from mod.delivery import Delivery

# HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
# HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i
HAND_X_RATE: Callable[[int], float] = lambda i: 42
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

# HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
# HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2
HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: -3
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60-HAND_Y_DIFF(i, j)/2*(j-1)+HAND_Y_DIFF(i, j)*i

# HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
# HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 4.0

def yamahuda_made_by_files(surfaces: list[Surface], delivery: Delivery, is_own: bool) -> Taba:
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
    huda.inject_funcs(draw=_draw, hover=_hover)
    
def _draw(huda: Huda) -> None:
    default_draw(huda=huda)
    IMG_YAMAHUDA.set_alpha(64)
    screen.blit(source=IMG_YAMAHUDA, dest=huda.img_rz_topleft)
    IMG_YAMAHUDA.set_alpha(255)
    # if controller.hover == huda:
    #     pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
    #     screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
    #     screen.blit(source=IMG_YAMAHUDA, dest=huda.img_rz_topleft+[0, -40])
    # else:
    #     default_draw(huda=huda)
    # return None

def _hover(huda: Huda) -> None:
    screen.blit(source=huda.img_nega, dest=[WX-huda.img_nega.get_width(), 0])
