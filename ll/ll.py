import pygame

from any.screen import clock, FRAMES_PER_SECOND
from any.propagation import propagation
from any.timer_functions import start_timer, end_timer
from seed.default_gm import gm
from ptc.view import View

# def mainloop(view: View) -> None:
#     start_timer()

#     propagation.resolve_pygame_events(get_hover=view.get_hover())
#     view.draw()
#     # from any.timer_functions import frames
#     # from any.screen import screen, WX, WY
#     # from any.font import MS_MINCHO_COL
#     # screen.blit(
#     #     source=MS_MINCHO_COL(f"{frames()}frames", 64, "black"),
#     #     dest=(WX/2, WY/2)
#     # )
#     propagation.mouse_over()

#     end_timer()
#     pygame.display.update()
#     clock.tick(FRAMES_PER_SECOND)

while True:
    gm.mainloop()
    # mainloop(view=gm.view)
