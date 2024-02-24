import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from math import sin, cos, radians
from typing import Callable, Any

from mod.const import screen, BLACK, BRIGHT, HUDA_SCALE
from mod.controller import controller

class HudaDraw():
    def __init__(self, x: int | float, y: int | float, angle: float, 
                 update_func: Callable[['HudaDraw'], None], huda: Any) -> None:
        self.x = int(x)
        self.y = int(y)
        self.img_detail = Surface((16, 16))
        self.img_rz = Surface((16, 16))
        self.img_rz_topleft = Vector2(0, 0)
        self.vertices = [Vector2(0, 0)]*4
        self.update_func = update_func
        self.huda = huda
        self.rearrange(x=x, y=y, angle=angle)

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
        if controller.hover == self.huda:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in self.vertices], 20)
            self.default_draw(offset=[0, -40])
        else:
            self.default_draw()

    def rearrange(self, x: int | float, y: int | float, angle: float) -> None:
        from mod.huda.huda_add_draw import img_detail
        self.x = int(x)
        self.y = int(y)
        self.img_detail = img_detail(huda=self.huda)
        self.img_rz = pygame.transform.rotozoom(surface=self.img_detail, angle=angle, scale=HUDA_SCALE)
        self.img_rz_topleft = Vector2(x, y)-Vector2(self.img_rz.get_size())/2
        self.vertices = [self.rotated_verticle(x, y, angle) for x, y in [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]]

    def rotated_verticle(self, x: int | float, y: int | float, angle: float) -> Vector2:
        rad = radians(-angle)
        return Vector2(int(self.x+(cos(rad)*x-sin(rad)*y)*HUDA_SCALE), int(self.y+(sin(rad)*x+cos(rad)*y)*HUDA_SCALE))
