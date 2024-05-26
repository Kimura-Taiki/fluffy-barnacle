import pygame

from any.timer_functions import start_timer, end_timer
from any.propagation import propagation
from any.screen import clock, FRAMES_PER_SECOND
from model.board import Board
from ptc.view import View, EMPTY_VIEW
from ptc.notification import Notification

from ptc.listener import Listener
class GameMaster():
    def __init__(self, board: Board, view: View=EMPTY_VIEW) -> None:
        self.board = board
        self.view = view

    def listen(self, nf: Notification) -> None:
        self.board = nf.created_board(board=self.board)

    def mainloop(self) -> None:
        start_timer()

        propagation.resolve_pygame_events(get_hover=self.view.get_hover())
        self.view.draw()
        # from any.timer_functions import frames
        # from any.screen import screen, WX, WY
        # from any.font import MS_MINCHO_COL
        # screen.blit(
        #     source=MS_MINCHO_COL(f"{frames()}frames", 64, "black"),
        #     dest=(WX/2, WY/2)
        # )
        propagation.mouse_over()

        end_timer()
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

