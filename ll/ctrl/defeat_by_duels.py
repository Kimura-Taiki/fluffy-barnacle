from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

class DefeatByDuelsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=f"決闘に敗れた{player.name}は脱落します"
        ))
