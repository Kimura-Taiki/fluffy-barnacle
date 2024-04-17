import pygame

from mod.const.screen import clock, FRAMES_PER_SECOND
from mod.router import router
from mod.banmen_view import BanmenView
from mod.banmen import Banmen

view = BanmenView()

def mainloop() -> None:
    router.resolve_pygame_events()
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
