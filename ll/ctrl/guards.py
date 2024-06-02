from any.font import MS_MINCHO_COL
from ctrl.messages import MessagesController
from model.kard import Kard
from ptc.bridge import Bridge

_FONT = 28

class GuardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, kard: Kard) -> None:
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"「{kard.name}」の効果は「僧侶」に防がれます", _FONT, "black"),
        ).action()
