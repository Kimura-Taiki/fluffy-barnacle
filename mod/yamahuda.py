#                 20                  40                  60                 79
from pygame.surface import Surface
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, IMG_YAMAHUDA, SIMOTE, KAMITE
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.delivery import Delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 42
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: -3
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60-HAND_Y_DIFF(i, j)/2*(j-1)+HAND_Y_DIFF(i, j)*i

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 4.0

def yamahuda_made_by_files(surfaces: list[Surface], delivery: Delivery, gata: int) -> Taba:
    tehuda = Taba(delivery=delivery, gata=gata, inject=_inject_of_tehuda)
    tehuda.var_rearrange = partial(_rearrange_tehuda, taba=tehuda)
    for i in surfaces:
        tehuda.append(Huda(img=i))
    return tehuda

def _rearrange_tehuda(taba: Taba) -> None:
    angle_func, x_func, y_func = _rearrange_funcs(l=len(taba), gata=taba.gata)
    [huda.rearrange(angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i)) for i, huda in enumerate(taba)]

def _rearrange_funcs(l: int, gata: int) -> tuple[Callable[[int], float], Callable[[int], float], Callable[[int], float]]:
    if gata == SIMOTE:
        return partial(HAND_ANGLE, j=l), partial(HAND_X, j=l), partial(HAND_Y, j=l)
    elif gata == KAMITE:
        return (partial(lambda i, j: HAND_ANGLE(i, j)+180.0, j=l),
                partial(lambda i, j: WX-HAND_X(i, j), j=l), partial(lambda i, j: WY-HAND_Y(i, j), j=l))

def _inject_of_tehuda(huda: Huda, taba: Taba) -> None:
    huda.inject_funcs(draw=_draw, hover=Huda.detail_draw)

def _draw(huda: Huda) -> None:
    default_draw(huda=huda)
    IMG_YAMAHUDA.set_alpha(64)
    screen.blit(source=IMG_YAMAHUDA, dest=huda.img_rz_topleft)
    IMG_YAMAHUDA.set_alpha(255)
