#                 20                  40                  60                 79
from typing import Any, Callable

from mod.const import compatible_with, pass_func, PH_NONE, PH_START, PH_MAIN, PH_END, opponent, side_name,\
    POP_START_PHASE_FINISHED, POP_MAIN_PHASE_FINISHED, POP_END_PHASE_FINISHED

from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery, duck_delivery
from mod.ol.start_phase import StartPhase
from mod.ol.main_phase import MainPhase
from mod.ol.over_layer import OverLayer
from mod.ol.pop_stat import PopStat

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

    def close(self) -> PopStat:
        return PopStat()

    def moderate(self, stat: PopStat) -> None:
        if stat.code == POP_MAIN_PHASE_FINISHED:
            self.turn += 1
            self.delivery.turn_player = opponent(self.delivery.turn_player)
            self.reset_name()
            moderator.append(StartPhase(inject_func=self.inject_func))
        elif stat.code == POP_START_PHASE_FINISHED:
            self.reset_name()
            moderator.append(MainPhase(inject_func=self.main_inject))

    def reset_name(self) -> None:
        self.name = f"{self.turn}ターン目 {side_name(self.delivery.turn_player)}"

compatible_with(TurnProgression(delivery=duck_delivery, main_inject=pass_func), OverLayer)
