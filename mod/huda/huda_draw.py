#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from math import sin, cos, radians
from typing import Callable, Any

from mod.const import screen, BLACK, BRIGHT, HUDA_SCALE
from mod.controller import controller

class HudaDraw():
    def __init__(self, img: Surface, x: int | float, y: int | float, angle: float, scale: float,
                 update_func: Callable[['HudaDraw'], None], huda: Any) -> None:
        self.x = int(x)
        self.y = int(y)
        self.scale = scale
        self.img_nega = img
        self.img_detail = Surface((16, 16))
        self.img_rz = Surface((16, 16))
        self.img_rz_topleft = Vector2(0, 0)
        self.vertices = [Vector2(0, 0)]*4
        self.update_func = update_func
        self.huda = huda

    def is_cursor_on(self) -> bool:
        inside = False
        mx, my = pygame.mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return inside

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

    def rearrange(self, x: int | float, y: int | float, angle: float, scale: float=HUDA_SCALE) -> None:
        from mod.huda.huda_add_draw import img_detail
        self.x = int(x)
        self.y = int(y)
        self.img_detail = img_detail(huda=self.huda)
        self.img_rz = pygame.transform.rotozoom(surface=self.img_detail, angle=angle, scale=self.scale)
        self.img_rz_topleft = Vector2(x, y)-Vector2(self.img_rz.get_size())/2
        hx, hy = Vector2(self.img_nega.get_size())/2
        li = [[-hx, -hy], [hx, -hy], [hx, hy], [-hx, hy]]
        self.vertices = [self.rotated_verticle(x, y, angle) for x, y in li]

    def rotated_verticle(self, x: int | float, y: int | float, angle: float) -> Vector2:
        rad = radians(-angle)
        return Vector2(int(self.x+(cos(rad)*x-sin(rad)*y)*self.scale), int(self.y+(sin(rad)*x+cos(rad)*y)*self.scale))
