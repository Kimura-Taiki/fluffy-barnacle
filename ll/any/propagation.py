import pygame
import sys
from pygame import Vector2 as V2, QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from any.screen import screen
from ptc.element import Element

class Propagation():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hover: Element | None = None
        self.active: Element | None = None
        self.data_transfer: Element | None = None
        self.hold_coord: V2
        self.drag: bool = False

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
            elif event.type == MOUSEBUTTONUP:
                if self.data_transfer:
                    self.data_transfer.dragend()
                    self.data_transfer = None
                    self.drag = False
                    self.active = None
                elif self.active:
                    self.active.mouseup()
                    self.active = None

    def mouse_over(self) -> None:
        if self.data_transfer:
            self.data_transfer.drag()
            if self.hover:
                self.hover.hover()
        elif self.active:
            self.active.active()
        elif self.hover:
            self.hover.hover()

propagation = Propagation()