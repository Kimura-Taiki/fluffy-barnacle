from pygame import Surface

from ptc.bridge import Bridge
from view.board_view import BoardView
from view.message_view import MessageView

from ptc.controller import Controller
class MessagesController():
    def __init__(self, bridge: Bridge, img_mes: Surface) -> None:
        self.bridge = bridge
        self.img_mes = img_mes

    def action(self) -> None:
        board_view = self.bridge.view
        if not isinstance(board_view, BoardView):
            raise ValueError("MessagesController を起動する時はBoardViewでないと", self.bridge.view)
        self.bridge.whileloop(new_view=MessageView(
            board_view=board_view,
            img_mes=self.img_mes,
        )
)
