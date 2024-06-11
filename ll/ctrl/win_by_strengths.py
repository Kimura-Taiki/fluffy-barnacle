from any.locales import lomes
from model.player import Player
from ptc.bridge import Bridge
from view.message_view import MessageView

class WinByStrengthsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def action(self, player: Player) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=lomes(folder="board", key="win_by_strengths", player_name=player.name)
        ))
