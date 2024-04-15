import pygame
import sys
from pygame.math import Vector2 as V2
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from typing import Callable

from mod.const.screen import screen

# from mod.const import screen, nie
# from mod.youso import Youso

class Controller():
    def __init__(self) -> None:
        ...
        # self.clicked: bool = False
        # self.hover: Youso | None = None
        # self.get_hover: Callable[[], Youso | None] = nie(text="Controller.get_hover")
        # self.active: Youso | None = None
        # self.data_transfer: Youso | None = None
        # self.hold_coord: V2
        # self.drag: bool = False

    def resolve_pygame_events(self) -> None:
        # self.hover = self.get_hover()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.image.save(screen, "screenshot.png")
                pygame.quit()
                sys.exit()
            # elif event.type == MOUSEBUTTONDOWN:
            #     if self.hover:
            #         self.hover.mousedown()
            # elif event.type == MOUSEBUTTONUP:
            #     if self.data_transfer:
            #         self.data_transfer.dragend()
            #         self.data_transfer = None
            #         self.drag = False
            #         self.active = None
            #     elif self.active:
            #         self.active.mouseup()
            #         self.active = None


    # def mouse_over(self) -> None:
    #     if self.data_transfer:
    #         self.data_transfer.drag()
    #         if self.hover:
    #             self.hover.hover()
    #     elif self.active:
    #         self.active.active()
    #     elif self.hover:
    #         self.hover.hover()

controller = Controller()