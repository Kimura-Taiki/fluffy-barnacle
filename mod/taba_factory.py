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
    def __init__(self, delivery: Delivery, hoyuusya: int, inject_kwargs: dict[str, Callable[[Huda], None]],
                 rearrange: Callable[[Taba], None], huda_x: Callable[[int, int], float], huda_y: Callable[[int, int], float],
                 huda_angle: Callable[[int, int], float]) -> None:
        self.delivery, self.hoyuusya, self.inject_kwargs, self.rearrange = delivery, hoyuusya, inject_kwargs, rearrange
        self.huda_x, self.huda_y, self.huda_angle = huda_x, huda_y, huda_angle
        self.simote_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: huda_x(i, j), lambda i, j: huda_y(i, j), lambda i, j: huda_angle(i, j))
        self.kamite_funcs: tuple[Callable[[int, int], float], Callable[[int, int], float], Callable[[int, int], float]] = (
            lambda i, j: WX-huda_x(i, j), lambda i, j: WY-huda_y(i, j), lambda i, j: huda_angle(i, j)+180.0)
        
    def maid_by_files(self, surfaces: list[Surface], delivery: Delivery, hoyuusya: int) -> Taba:
        taba = Taba(delivery=delivery, hoyuusya=hoyuusya, inject=_inject_of_tehuda)
        taba.rearrange = partial(self._rearrange_huda, taba=taba)
        for i in surfaces:
            taba.append(Huda(img=i))
        return taba

    def _rearrange_huda(self, taba: Taba) -> None:
        if not (funcs := {SIMOTE: self.simote_funcs, KAMITE: self.kamite_funcs}.get(self.hoyuusya)):
            raise ValueError(f"Invalid TabaFactory.hoyuusya: {self.hoyuusya}")
        l = len(taba)
        x_func, y_func, a_func = partial(funcs[0], j=l), partial(funcs[1], j=l), partial(funcs[2], j=l)
        for i, huda in enumerate(taba):
            huda.rearrange(angle=a_func(i), scale=0.6, x=x_func(i), y=y_func(i))

    def _inject(self, huda: Huda, taba: Taba) -> None:
        # huda.inject_funcs(draw=_draw, hover=Huda.detail_draw, mousedown=_mousedown, active=_active,
        #                 mouseup=partial(_mouseup, delivery=taba.delivery),drag=_drag)
        huda.inject_funcs(**self.inject_kwargs)


def tehuda_made_by_files(surfaces: list[Surface], delivery: Delivery, hoyuusya: int) -> Taba:
    tehuda = Taba(delivery=delivery, hoyuusya=hoyuusya, inject=_inject_of_tehuda)
    tehuda.rearrange = partial(_rearrange_tehuda, taba=tehuda)
    for i in surfaces:
        tehuda.append(Huda(img=i))
    return tehuda

def _rearrange_tehuda(taba: Taba) -> None:
    angle_func, x_func, y_func = _rearrange_funcs(l=len(taba), hoyuusya=taba.hoyuusya)
    [huda.rearrange(angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i)) for i, huda in enumerate(taba)]

def _rearrange_funcs(l: int, hoyuusya: int) -> tuple[Callable[[int], float], Callable[[int], float], Callable[[int], float]]:
    if hoyuusya == SIMOTE:
        return partial(HAND_ANGLE, j=l), partial(HAND_X, j=l), partial(HAND_Y, j=l)
    elif hoyuusya == KAMITE:
        return (partial(lambda i, j: HAND_ANGLE(i, j)+180.0, j=l),
                partial(lambda i, j: WX-HAND_X(i, j), j=l), partial(lambda i, j: WY-HAND_Y(i, j), j=l))

def _inject_of_tehuda(huda: Huda, taba: Taba) -> None:
    huda.inject_funcs(draw=_draw, hover=Huda.detail_draw, mousedown=_mousedown, active=_active,
                      mouseup=partial(_mouseup, delivery=taba.delivery),drag=_drag)

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

def _mouseup(huda: Huda, delivery: Delivery) -> None:
    if (pygame.mouse.get_pos()-controller.hold_coord).length_squared() < 50: return
    delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

def _mouseup(huda: Huda) -> None:
    if (pygame.mouse.get_pos()-controller.hold_coord).length_squared() < 50: return
    huda.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

def _drag(huda: Huda) -> None:
    gpv2 = Vector2(pygame.mouse.get_pos())
    pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.vertices], 20)
    huda.img_rz.set_alpha(192)
    screen.blit(source=huda.img_rz, dest=gpv2-Vector2(huda.img_rz.get_size())/2)
    huda.img_rz.set_alpha(255)
