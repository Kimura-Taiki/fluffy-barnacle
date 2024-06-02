from any.font import MS_MINCHO_COL
from ctrl.messages import MessagesController
from model.player import Player
from ptc.bridge import Bridge

_FONT = 28

class DefeatsByMinistersController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player) -> None:
        MessagesController(
            bridge=self.bridge,
            img_mes=MS_MINCHO_COL(f"「大臣」を含む強さの合計が12以上になったので{player.name}は脱落します", _FONT, "black"),
        ).action()
