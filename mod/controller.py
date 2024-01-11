import pygame
import sys
from pygame.locals import QUIT, MOUSEMOTION
from typing import Callable


from mod.youso import Youso

class Controller():
    def __init__(self) -> None:
        self.clicked: bool = False
        self.hover: Youso | None = None
        self.get_hover: Callable[[], Youso | None] = self._not_implemented_get_hover_youso
        self.active: Youso | None = None

    def resolve_pygame_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.hover = self.get_hover()

    def mouse_over(self) -> None:
        if self.hover:
            self.hover.hover()

    @staticmethod
    def _not_implemented_get_hover_youso() -> None:
        raise NotImplementedError("Controller.get_hover_yousoが未定義です")

controller = Controller()