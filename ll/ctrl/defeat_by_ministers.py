from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

class DefeatByMinistersController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=f"「大臣」を含む強さの合計が12以上になったので{player.name}は脱落します"
        ))
