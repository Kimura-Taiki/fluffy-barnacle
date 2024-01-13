import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, BRIGHT, ACTION_CIRCLE_NEUTRAL
from mod.huda import Huda, default_draw
from mod.taba import Taba
from mod.controller import controller

HAND_X_RATE = 120
HAND_ANGLE_RATE = -6.0
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE/2*(j-1)+HAND_ANGLE_RATE*i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE/2*(j-1)+HAND_X_RATE*i
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+abs(i*2-(j-1))**2*2

class Tehuda(Taba):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__(data)
        self.held_on: Huda | None = None

    def get_hover_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)

    def elapse(self) -> None:
        [huda.draw() for huda in self]

    @classmethod
    def made_by_files(cls, surfaces: list[Surface]) -> "Tehuda":
        j = len(surfaces)
        return Tehuda(data=[Huda(img=v, angle=HAND_ANGLE(i, j), scale=0.6, x=HAND_X(i, j), y=HAND_Y(i, j),
                                 draw=cls._draw_tehuda, hover=cls._hover_tehuda, dragstart=cls._dragstart_tehuda, drag=cls._drag_tehuda)
                            for i, v in enumerate(surfaces)])

    @staticmethod
    def _hover_tehuda(huda: Huda) -> None:
        screen.blit(source=huda.img_nega, dest=[WX-huda.img_nega.get_width(), 0])

    @staticmethod
    def _draw_tehuda(huda: Huda) -> None:
        if controller.active == huda:
            return None
        elif controller.hover == huda:
            pygame.draw.polygon(screen, BRIGHT, [[x, y-40] for x, y in huda.vertices], 20)
            screen.blit(source=huda.img_rz, dest=[huda.x-huda.img_rz.get_width()/2, huda.y-huda.img_rz.get_height()/2-40])
        else:
            default_draw(huda=huda)
        return None
    
    @staticmethod
    def _dragstart_tehuda(huda: Huda) -> None:
        controller.active = huda
        controller.hold_coord = Vector2(pygame.mouse.get_pos())
        # controller.hold_x, controller.hold_y = pygame.mouse.get_pos()
        # mx, my = pygame.mouse.get_pos()
        # controller.hold_x = mx-ACTION_CIRCLE_NEUTRAL.get_width()/2
        # controller.hold_y = my-ACTION_CIRCLE_NEUTRAL.get_height()/2
    
    @staticmethod
    def _drag_tehuda(huda: Huda) -> None:
        diff_coord = pygame.mouse.get_pos()-controller.hold_coord
        # mx, my = pygame.mouse.get_pos()
        if (rr := diff_coord.length_squared()) < 50:
            screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
        # if (rr := (controller.hold_x-mx)**2+(controller.hold_y-my)**2) < 50:
        #     screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=[controller.hold_x-250, controller.hold_y-250])
        # mx, my = pygame.mouse.get_pos()
        # pygame.draw.polygon(screen, BRIGHT, [[x-huda.x+mx, y-huda.y+my] for x, y in huda.vertices], 20)
        # huda.img_rz.set_alpha(192)
        # screen.blit(source=huda.img_rz, dest=[mx-huda.img_rz.get_width()/2, my-huda.img_rz.get_height()/2])
        # huda.img_rz.set_alpha(255)

