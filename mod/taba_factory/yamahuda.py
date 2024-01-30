#                 20                  40                  60                 79
from typing import Callable

from mod.const import WX, WY, screen, IMG_YAMAHUDA
from mod.huda import Huda, default_draw
from mod.taba_factory.taba_factory import TabaFactory

HAND_X_RATE: Callable[[int], float] = lambda i: 42
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: -3
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60-HAND_Y_DIFF(i, j)/2*(j-1)+HAND_Y_DIFF(i, j)*i

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 4.0

def _draw(huda: Huda) -> None:
    default_draw(huda=huda)
    IMG_YAMAHUDA.set_alpha(64)
    screen.blit(source=IMG_YAMAHUDA, dest=huda.img_rz_topleft)
    IMG_YAMAHUDA.set_alpha(255)

yamahuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw
}, huda_x=HAND_X, huda_y= HAND_Y, huda_angle=HAND_ANGLE)
