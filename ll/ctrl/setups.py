from dataclasses import dataclass
from typing import Callable
from ptc.bridge import Bridge

from ptc.controller import Controller
@dataclass
class SetupsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self) -> None:
        while (handless_player := next((
            player for player in self.bridge.board.players if len(player.hands) == 0
        ), None)):
            self.bridge.board.draw(player=handless_player)
        else:
            self._game_start()

    def _game_start(self) -> None:
        self.bridge.board.game_start()
        self.bridge.board.turn_start()
