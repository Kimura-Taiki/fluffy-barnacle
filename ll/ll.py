import pygame

from any.screen import clock, FRAMES_PER_SECOND
from any.router import router
from seed.default_gm import gm
from ptc.view import View

def mainloop(view: View) -> None:
    router.resolve_pygame_events(get_hover=view.get_hover())
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop(view=gm.view)
