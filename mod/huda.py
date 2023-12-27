import pygame
from pygame.surface import Surface
from math import sin, cos, radians

class Huda():

    def __init__(self, screen: Surface, img: Surface, angle: float=0.0, scale: float=0.4, x:int | float=0, y:int | float=0) -> None:
        self.screen = screen
        self.img_nega = img
        self.img_rz = pygame.transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.angle = angle
        self.scale = scale
        self.x = int(x)
        self.y = int(y)
        self.vertices = [self.rotated_verticle(i[0], i[1]) for i in [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]]
        print(self.vertices)

    def rotated_verticle(self, x:int | float, y:int | float) -> list[int]:
        rad = radians(-self.angle)
        return [int(self.x+(cos(rad)*x-sin(rad)*y)*self.scale), int(self.y+(sin(rad)*x+cos(rad)*y)*self.scale)]

    def draw(self) -> None:
        [pygame.draw.circle(surface=self.screen, color=(0, 0, 255), center=[i[0], i[1]], radius=10) for i in self.vertices]
        self.screen.blit(source=self.img_rz, dest=[self.x-self.img_rz.get_width()/2, self.y-self.img_rz.get_height()/2])

    def is_cursor_on(self) -> bool:
        return True

    @property
    def dest(self) -> [int, int]:
        return self.x, self.y
    
    @dest.setter
    def dest(self, x:int | float, y:int | float) -> None:
        self.x, self.y = int(x), int(y)

