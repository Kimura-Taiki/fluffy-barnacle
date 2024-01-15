import pygame
import sys
from pygame.event import Event
from pygame.math import Vector2 as V2
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from typing import Callable

from mod.const import screen, MS_MINCHO
from mod.youso import Youso

class Controller():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hover: Youso | None = None
        self.get_hover: Callable[[], Youso | None] = self._not_implemented_get_hover_youso
        self.active: Youso | None = None
        self.data_transfer: Youso | None = None
        self.hold_coord: V2
        self.drag: bool = False

    def resolve_pygame_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.hover = self.get_hover()
            elif event.type == MOUSEBUTTONDOWN:
                if self.hover:
                    self.hover.dragstart()
            elif event.type == MOUSEBUTTONUP:
                if self.active:
                    self.active.dragend()
                    self.active = None
                    self.drag = False


    def mouse_over(self) -> None:
        # screen.blit(source=MS_MINCHO(f"MM : {self.motion.pos}, {self.motion.rel}, {self.motion.buttons}", 32), dest=[0, 80])
        if self.hover:
            self.hover.hover()
        if self.active:
            self.active.drag()
            # self.active.

    @staticmethod
    def _not_implemented_get_hover_youso() -> None:
        raise NotImplementedError("Controller.get_hover_yousoが未定義です")

controller = Controller()