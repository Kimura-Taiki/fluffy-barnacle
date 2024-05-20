import pygame

from mod.screen import clock, FRAMES_PER_SECOND
from mod.router import router
# from mod.board_view import view
from mod.b_a_v import view

router.get_hover = view.get_hover

def mainloop() -> None:
    router.resolve_pygame_events()
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()