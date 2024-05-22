import pygame

from mod.screen import clock, FRAMES_PER_SECOND
from mod.router import router
# from mod.board_view import view
# from mod.b_a_v import view
from seed.default_gm import gm
from ptc.view import View

# router.get_hover = view.get_hover

# def mainloop() -> None:
def mainloop(view: View) -> None:
    # router.resolve_pygame_events()
    router.resolve_pygame_events(get_hover=view.get_hover())
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    # mainloop()
    mainloop(view=gm.view)
