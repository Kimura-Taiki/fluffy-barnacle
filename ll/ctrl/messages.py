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
        message_view = MessageView(
            board_view=self._old_view,
            img_mes=self.img_mes,
        )
        self.bridge.view = message_view
        self.bridge.whileloop(cond=message_view.in_progress)
        self.bridge.view = self._old_view
        self.suffix()
