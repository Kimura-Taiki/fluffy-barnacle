import pygame
import sys
from pygame.event import Event
from pygame.locals import QUIT, MOUSEMOTION
from typing import Callable

from mod.const import screen, MS_MINCHO
from mod.youso import Youso

class Controller():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hover: Youso | None = None
        self.get_hover: Callable[[], Youso | None] = self._not_implemented_get_hover_youso
        self.active: Youso | None = None
        self.motion: Event

    def resolve_pygame_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.motion = event
                self.hover = self.get_hover()

    def mouse_over(self) -> None:
        # screen.blit(source=MS_MINCHO(f"MM : {self.motion.pos}, {self.motion.rel}, {self.motion.buttons}", 32), dest=[0, 80])
        if self.hover:
            self.hover.hover()

    @staticmethod
    def _not_implemented_get_hover_youso() -> None:
        raise NotImplementedError("Controller.get_hover_yousoが未定義です")

controller = Controller()