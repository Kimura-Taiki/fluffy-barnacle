import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from math import sin, cos, radians
from typing import Callable

from mod.youso import Youso
from mod.const import screen, pass_func, BRIGHT
from mod.controller import controller

def default_draw(huda: 'Huda') -> None:
    screen.blit(source=huda.img_rz, dest=[huda.x-huda.img_rz.get_width()/2, huda.y-huda.img_rz.get_height()/2])

# class Huda(Youso):
#     def __init__(self, img: Surface, angle: float=0.0, scale: float=0.4, x:int | float=0, y:int | float=0,
#                  draw: Callable[..., None]=default_draw, hover: Callable[..., None]=pass_func,
#                  dragstart: Callable[..., None]=pass_func, drag: Callable[..., None]=pass_func,
#                  dragend: Callable[..., None]=pass_func) -> None:
#         super().__init__(draw=draw, hover=hover, dragstart=dragstart, drag=drag, dragend=dragend)
class Huda(Youso):
    def __init__(self, img: Surface, angle: float=0.0, scale: float=0.4, x:int | float=0, y:int | float=0,
                 draw: Callable[..., None]=default_draw, **kwargs) -> None:
        super().__init__(draw=draw, **kwargs)
        self.img_nega = img
        self.img_rz = pygame.transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.angle = angle
        self.scale = scale
        self.x = int(x)
        self.y = int(y)
        self.vertices = [self.rotated_verticle(i[0], i[1]) for i in [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]]

    def rotated_verticle(self, x:int | float, y:int | float) -> list[int]:
        rad = radians(-self.angle)
        return [int(self.x+(cos(rad)*x-sin(rad)*y)*self.scale), int(self.y+(sin(rad)*x+cos(rad)*y)*self.scale)]

    def is_cursor_on(self) -> bool:
        inside = False
        mx, my = pygame.mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return inside

    @property
    def dest(self) -> Vector2:
        return Vector2(self.x, self.y)
    
    @dest.setter
    def dest(self, x:int | float, y:int | float) -> None:
        self.x, self.y = int(x), int(y)
