#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, BRIGHT
from mod.huda.huda import Huda
from mod.controller import controller
from mod.tf.taba_factory import TabaFactory
from mod.kd.action_circle import mousedown, active, mouseup

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    else:
        huda.available_draw()

def _drag(huda: Huda) -> None:
    img_rz = huda.huda_draw.img_rz
    gpv2 = Vector2(pygame.mouse.get_pos())
    pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.huda_draw.vertices], 20)
    img_rz.set_alpha(192)
    screen.blit(source=img_rz, dest=gpv2-Vector2(img_rz.get_size())/2)
    img_rz.set_alpha(255)

tehuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw, "mousedown": mousedown, "active": active, "mouseup": mouseup, "drag": _drag
    }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
