#                 20                  40                  60                 79
from typing import Callable

from mod.const import pass_func, POP_END_PHASE_FINISHED, POP_END_TRIGGERED,\
    POP_DISCARDED, TG_END_PHASE, enforce
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.moderator import moderator
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.coous.trigger import solve_trigger_effect

class EndPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "終了フェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        solve_trigger_effect(delivery=self.delivery, hoyuusya=self.hoyuusya, trigger=TG_END_PHASE, code=POP_END_TRIGGERED)
        if moderator.last_layer() == self:
            self.moderate(PopStat(code=POP_END_TRIGGERED))

    def close(self) -> PopStat:
        return PopStat(POP_END_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        enforce({POP_END_TRIGGERED: self._end_triggered,
                 POP_DISCARDED: self._discarded
                 }.get(stat.code), type(self.moderate))(stat=stat)

    def _end_triggered(self, stat: PopStat) -> None:
        if moderator.last_layer() == self:
            self.moderate(PopStat(code=POP_DISCARDED))

    def _discarded(self, stat: PopStat) -> None:
        popup_message.add(text="ターンを終了します")
        moderator.pop()