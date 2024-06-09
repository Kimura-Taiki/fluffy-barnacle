from model.kard import Kard
from ptc.bridge import Bridge
from view.message_view import MessageView

class GuardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, kard: Kard) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=f"「{kard.name}」の効果は「僧侶」に防がれます"
        ))
