import pygame
from typing import Callable

from any.timer_functions import start_timer, end_timer
from any.mouse_dispatcher import mouse_dispatcher
from any.screen import clock, FRAMES_PER_SECOND
from model.board import Board
from ptc.view import View, EMPTY_VIEW

from ptc.bridge import Bridge
class GameMaster():
    def __init__(self, board: Board, view: View=EMPTY_VIEW) -> None:
        self.board = board
        self.view = view

    def mainloop(self) -> None:
        start_timer()

        mouse_dispatcher.resolve_pygame_events(get_hover=self.view.get_hover())
        self.view.draw()
        self.view.elapse()
        # from any.timer_functions import frames
        # from any.screen import screen, WX, WY
        # from any.font import MS_MINCHO_COL
        # screen.blit(
        #     source=MS_MINCHO_COL(f"{frames()}frames", 64, "black"),
        #     dest=(WX/2, WY/2)
        # )
        mouse_dispatcher.mouse_over()

        end_timer()
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

    def whileloop(self, cond: Callable[[], bool]) -> None:
        while cond():
            self.mainloop()