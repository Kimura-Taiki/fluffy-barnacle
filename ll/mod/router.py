import pygame
import sys
from pygame.math import Vector2 as V2
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from typing import Callable

from mod.screen import screen
from mod.func import nie
from ptc.element import Element

class Router():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hover: Element | None = None
        # self.get_hover: Callable[[], Element | None] = nie(text="Controller.get_hover")
        self.active: Element | None = None
        self.data_transfer: Element | None = None
        self.hold_coord: V2
        self.drag: bool = False

    # def resolve_pygame_events(self) -> None:
    #     self.hover = self.get_hover()
    def resolve_pygame_events(self, get_hover: Element | None) -> None:
        self.hover = get_hover
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.image.save(screen, "ll/screenshot.png")
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.hover:
                    self.hover.mousedown()
            # elif event.type == MOUSEBUTTONUP:
            #     if self.data_transfer:
            #         self.data_transfer.dragend()
            #         self.data_transfer = None
            #         self.drag = False
            #         self.active = None
            #     elif self.active:
            #         self.active.mouseup()
            #         self.active = None


    def mouse_over(self) -> None:
        if self.data_transfer:
            self.data_transfer.drag()
            if self.hover:
                self.hover.hover()
        elif self.active:
            self.active.active()
        elif self.hover:
            self.hover.hover()

router = Router()