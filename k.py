import pygame

from mod.const.screen import screen, clock, FRAMES_PER_SECOND, IMG_YATUBA_BG
from mod.controller import controller

class Viewer():
    def __init__(self) -> None:
        pass

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        ...

viewer = Viewer()

def mainloop() -> None:
    controller.resolve_pygame_events()
    viewer.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
