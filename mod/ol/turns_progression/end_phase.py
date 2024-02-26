#                 20                  40                  60                 79
from typing import Callable

from mod.const import pass_func, POP_END_PHASE_FINISHED
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.moderator import moderator
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.coous.end_phase_trigger import end_phase_trigger

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
        end_phase_trigger(delivery=self.delivery, hoyuusya=self.hoyuusya)
        if moderator.last_layer() == self:
            moderator.pop()

    def close(self) -> PopStat:
        popup_message.add(text="ターンを終了します")
        return PopStat(POP_END_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        moderator.pop()
