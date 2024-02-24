import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from typing import Callable

from mod.const import screen, BLACK, BRIGHT
from mod.controller import controller

class HudaDraw():
    def __init__(self, img_detail: Surface, img_rz: Surface, img_rz_topleft: Vector2, vertices: list[Vector2],
                 update_func: Callable[['HudaDraw'], None]) -> None:
        self.img_detail = img_detail
        self.img_rz = img_rz
        self.img_rz_topleft = img_rz_topleft
        self.vertices = vertices
        self.update_func = update_func

    def detail_draw(self) -> None:
        screen.blit(source=self.img_detail, dest=[0, 0])

    def default_draw(self, offset: Vector2 | tuple[int, int] | list[int]=(0, 0)) -> None:
        self.update_func(self)
        screen.blit(source=self.img_rz, dest=self.img_rz_topleft+offset)

    def shadow_draw(self) -> None:
        pygame.draw.polygon(surface=screen, color=BLACK, points=self.vertices, width=0)
        self.img_rz.set_alpha(192)
        self.default_draw()
        self.img_rz.set_alpha(255)

    def available_draw(self) -> None:
        if controller.hover == self:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in self.vertices], 20)
            self.default_draw(offset=[0, -40])
        else:
            self.default_draw()
