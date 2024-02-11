#                 20                  40                  60                 79
from typing import Any, Callable

from mod.const import compatible_with, pass_func, PH_NONE, PH_MAIN, opponent, side_name
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery, duck_delivery
from mod.ol.main_phase import MainPhase
from mod.ol.over_layer import OverLayer

class TurnProgression():
    def __init__(self, delivery: Delivery, main_inject: Callable[[], None]) -> None:
        self.name = "1ターン目 下手"
        self.inject_func: Callable[[], None] = pass_func
        self.main_inject = main_inject
        self.phase = PH_NONE
        self.delivery: Delivery = delivery
        self.turn = 1

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        moderator.append(MainPhase(inject_func=self.main_inject))
        self.turn = 1
        self.phase = PH_MAIN
        self.reset_name()

    def close(self) -> Any:
        ...

    def moderate(self, stat: int) -> None:
        if self.phase == PH_MAIN:
            self.turn += 1
            self.delivery.turn_player = opponent(self.delivery.turn_player)
            self.reset_name()
            moderator.append(MainPhase(inject_func=self.main_inject))
        
    def reset_name(self) -> None:
        self.name = f"{self.turn}ターン目 {side_name(self.delivery.turn_player)}"

compatible_with(TurnProgression(delivery=duck_delivery, main_inject=pass_func), OverLayer)
