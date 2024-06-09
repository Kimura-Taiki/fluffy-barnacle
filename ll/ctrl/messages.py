from pygame import Surface

from ptc.bridge import Bridge
from view.message_view import MessageView

from ptc.controller import Controller
class MessagesController():
    def __init__(self, bridge: Bridge, img_mes: Surface) -> None:
        self.bridge = bridge
        self.img_mes = img_mes

    def action(self) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=self.img_mes,
        )
)
