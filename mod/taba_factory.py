#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, BRIGHT, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_CARD, ACTION_CIRCLE_BASIC, TC_HUSEHUDA\
    , SIMOTE, KAMITE, HANTE
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller
from mod.delivery import Delivery, duck_delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class TabaFactory():
    def __init__(self, delivery: Delivery, inject_kwargs: dict[str, Callable[[Huda], None]],
                 huda_x: Callable[[int, int], float], huda_y: Callable[[int, int], float],
                 huda_angle: Callable[[int, int], float]) -> None:
        self.delivery, self.inject_kwargs = delivery, inject_kwargs
        self.huda_x, self.huda_y, self.huda_angle = huda_x, huda_y, huda_angle
        self.simote_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: huda_x(i, j), lambda i, j: huda_y(i, j), lambda i, j: huda_angle(i, j))
        self.kamite_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: WX-huda_x(i, j), lambda i, j: WY-huda_y(i, j), lambda i, j: huda_angle(i, j)+180.0)
        
    def maid_by_files(self, surfaces: list[Surface], delivery: Delivery, hoyuusya: int) -> Taba:
        taba = Taba(delivery=delivery, hoyuusya=hoyuusya, inject=self._inject)
        taba.rearrange = partial(self._rearrange_huda, taba=taba, hoyuusya=hoyuusya)
        for i in surfaces:
            taba.append(Huda(img=i))
        return taba

    def _rearrange_huda(self, taba: Taba, hoyuusya: int) -> None:
        if not (funcs := {SIMOTE: self.simote_funcs, KAMITE: self.kamite_funcs}.get(hoyuusya)):
            raise ValueError(f"Invalid hoyuusya: {hoyuusya}")
        l = len(taba)
        x_func, y_func, a_func = partial(funcs[0], j=l), partial(funcs[1], j=l), partial(funcs[2], j=l)
        for i, huda in enumerate(taba):
            huda.rearrange(angle=a_func(i), scale=0.6, x=x_func(i), y=y_func(i))

    def _inject(self, huda: Huda, taba: Taba) -> None:
        huda.inject_funcs(**self.inject_kwargs)


def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    elif controller.hover == huda:
        pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
        screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
    else:
        default_draw(huda=huda)
    return None

def _mousedown(huda: Huda) -> None:
    controller.active = huda
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def _active(huda: Huda) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        controller.data_transfer = huda
    else:
        if 30 <= (deg := diff_coord.angle_to([0, 0])) and deg < 150:
            screen.blit(source=ACTION_CIRCLE_CARD, dest=controller.hold_coord-[250, 250])
        else:
            screen.blit(source=ACTION_CIRCLE_BASIC, dest=controller.hold_coord-[250, 250])

def _mouseup(huda: Huda) -> None:
    if (pygame.mouse.get_pos()-controller.hold_coord).length_squared() < 50: return
    huda.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

def _drag(huda: Huda) -> None:
    gpv2 = Vector2(pygame.mouse.get_pos())
    pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.vertices], 20)
    huda.img_rz.set_alpha(192)
    screen.blit(source=huda.img_rz, dest=gpv2-Vector2(huda.img_rz.get_size())/2)
    huda.img_rz.set_alpha(255)


tehuda_factory = TabaFactory(delivery=duck_delivery, inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active, "mouseup": _mouseup, "drag": _drag
    }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)