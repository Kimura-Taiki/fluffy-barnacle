#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable
from functools import partial

from mod.const import WX, WY, screen, BRIGHT, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_CARD, ACTION_CIRCLE_BASIC, TC_HUSEHUDA
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller
from mod.delivery import Delivery

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class Tehuda(Taba):
    def __init__(self, delivery: Delivery, data: list[Huda]=[], is_own: bool=True) -> None:
        super().__init__(data)
        self.delivery: Delivery = delivery
        self.is_one = is_own

    def rearrange(self) -> None:
        angle_func, x_func, y_func = self._rearrange_funcs(l=len(self), is_own=self.is_one)
        [huda.rearrange(angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i)) for i, huda in enumerate(self)]

    @classmethod
    def _rearrange_funcs(cls, l: int, is_own: bool) -> tuple[Callable[[int], float], Callable[[int], float], Callable[[int], float]]:
        if is_own:
            return partial(HAND_ANGLE, j=l), partial(HAND_X, j=l), partial(HAND_Y, j=l)
        else:
            return (partial(lambda i, j: HAND_ANGLE(i, j)+180.0, j=l),
                    partial(lambda i, j: WX-HAND_X(i, j), j=l), partial(lambda i, j: WY-HAND_Y(i, j), j=l))

    @classmethod
    def made_by_files(cls, surfaces: list[Surface], delivery: Delivery, is_own: bool) -> "Tehuda":
        angle_func, x_func, y_func = cls._rearrange_funcs(l=len(surfaces), is_own=is_own)
        return Tehuda(data=[Huda(img=v, angle=angle_func(i), scale=0.6, x=x_func(i), y=y_func(i),
                                 draw=cls._draw_tehuda, hover=cls._hover_tehuda, mousedown=cls._mousedown_tehuda,
                                 active=cls._active_huda, mouseup=partial(cls._mouseup_tehdua, delivery=delivery),
                                 drag=cls._drag_tehuda)
                            for i, v in enumerate(surfaces)], delivery=delivery, is_own=is_own)

    @staticmethod
    def _draw_tehuda(huda: Huda) -> None:
        if controller.active == huda:
            return None
        elif controller.hover == huda:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
            screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
        else:
            default_draw(huda=huda)
        return None

    @staticmethod
    def _hover_tehuda(huda: Huda) -> None:
        screen.blit(source=huda.img_nega, dest=[WX-huda.img_nega.get_width(), 0])

    @staticmethod
    def _mousedown_tehuda(huda: Huda) -> None:
        controller.active = huda
        controller.hold_coord = Vector2(pygame.mouse.get_pos())

    @staticmethod
    def _active_huda(huda: Huda) -> None:
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

    @staticmethod
    def _mouseup_tehdua(huda: Huda, delivery: Delivery) -> None:
        if (pygame.mouse.get_pos()-controller.hold_coord).length_squared() < 50: return
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

    @staticmethod
    def _drag_tehuda(huda: Huda) -> None:
        gpv2 = Vector2(pygame.mouse.get_pos())
        pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.vertices], 20)
        huda.img_rz.set_alpha(192)
        screen.blit(source=huda.img_rz, dest=gpv2-Vector2(huda.img_rz.get_size())/2)
        huda.img_rz.set_alpha(255)
