from pygame import Surface
from typing import Callable

from ptc.bridge import Bridge
from view.board_view import BoardView
from view.message_view import MessageView

from ptc.controller import Controller
class MessagesController():
    def __init__(self, bridge: Bridge, img_mes: Surface, suffix: Callable[[], None]=lambda : None) -> None:
        self.bridge = bridge
        if not isinstance(self.bridge.view, BoardView):
            raise ValueError("MessagesController を起動する時はBoardViewでないと", self.bridge.view)
        self._old_view = self.bridge.view
        self.img_mes = img_mes
        self.suffix = suffix

    def action(self) -> None:
        self.bridge.view = MessageView(
            board_view=self._old_view,
            img_mes=self.img_mes,
            callback=self._draw_callback
        )

    def _draw_callback(self) -> None:
        self.bridge.view = self._old_view
        self.suffix()
