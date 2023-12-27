import pygame
from pygame.locals import QUIT
import sys
from math import sin, cos, radians

WX = 800
WY = 600
FRAMES_PER_SECOND = 30

pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

img = pygame.image.load("cards/na_00_hajimari_a_n_1.png").convert_alpha()   # 340x475
mini_img = pygame.transform.rotozoom(surface=img, angle=90.0, scale=0.4)     # 68x190

class Huda():
    from pygame.surface import Surface

    coord_diff = [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]

    def __init__(self, screen: Surface, img: Surface, angle: float=0.0, scale: float=0.4, x:int | float=0, y:int | float=0) -> None:
        self.screen = screen
        self.img_nega = img
        self.img_rz = pygame.transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.angle = angle
        self.scale = scale
        self.x = int(x)
        self.y = int(y)
        self.vertices = []

    def rotated_verticle(self, x:int | float, y:int | float) -> list[int]:
        rad = radians(-self.angle)
        return int(self.x+cos(rad)*x-sin(rad)*y), int(self.y+sin(rad)*x+cos(rad)*y)

    def draw_huda(self) -> None:
        self.screen.blit(source=self.img_rz, dest=[self.x, self.y])

    @property
    def dest(self) -> [int, int]:
        return self.x, self.y
    
    @dest.setter
    def dest(self, x:int | float, y:int | float) -> None:
        self.x, self.y = int(x), int(y)

huda = Huda(screen=screen, img=pygame.image.load("cards/na_00_hajimari_a_n_1.png").convert_alpha(),
            angle=90.0, scale=0.4, x=100, y=100)

def mainloop() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(color=(255, 255, 128))
    huda.draw_huda()
    # screen.blit(source=mini_img, dest=[100, 100])
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
