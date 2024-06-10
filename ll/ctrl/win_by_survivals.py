from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

class WinBySurvivalsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=f"生き残った{player.name}が勝利しました"
        ))
