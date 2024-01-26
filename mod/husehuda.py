#                 20                  40                  60                 79
from typing import Callable

from mod.const import WX, WY, screen, IMG_BACK
from mod.huda import Huda
from mod.taba_factory import TabaFactory

HAND_X: Callable[[int, int], int | float] = lambda i, j: 340+286/2

HAND_Y_DIFF: Callable[[int], float] = lambda i: -36 if i < 4 else -144/i
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-102+HAND_Y_DIFF(j)*i

HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: 90.0

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

husehuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw
}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
