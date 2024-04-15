import pygame
from typing import Protocol, runtime_checkable

from mod.const.screen import screen, clock, FRAMES_PER_SECOND, IMG_YATUBA_BG
from mod.router import router

class Banmen():
    def __init__(self) -> None:
        pass

class View():
    def __init__(self) -> None:
        ...

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        ...

view = View()

def mainloop() -> None:
    router.resolve_pygame_events()
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
