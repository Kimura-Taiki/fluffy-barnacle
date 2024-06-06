from any.font import MS_MINCHO_COL
from ctrl.messages import MessagesController
from model.player import Player
from ptc.bridge import Bridge

_FONT = 28

class PeepsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, peeper: Player, watched: Player, subject: Player) -> None:
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"{peeper.name}は{watched.name}の手札を覗きました", _FONT, "black"),
        ).action()
