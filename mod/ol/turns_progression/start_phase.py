#                 20                  40                  60                 79
from typing import Callable

from mod.const import pass_func, POP_START_PHASE_FINISHED, UC_ZYOGAI, UC_SYUUTYUU, side_name,\
    POP_HUYO_ELAPSED, POP_RESHUFFLED, enforce, SIMOTE, KAMITE
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.ol.remove_osame.remove_osame import RemoveOsame
from mod.moderator import moderator
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.ol.reshuffle import reshuffle_layer

class StartPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "開始フェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        popup_message.add(f"{side_name(self.hoyuusya)}のターンです")
        self.delivery.b_params.start_turn()
        self.delivery.m_params(hoyuusya=SIMOTE).start_turn()
        self.delivery.m_params(hoyuusya=KAMITE).start_turn()
        self.delivery.send_ouka_to_ryouiki(
            hoyuusya=self.hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU)
        popup_message.add("集中力を１得ます")
        moderator.append(RemoveOsame(delivery=self.delivery, hoyuusya=self.hoyuusya))

    def close(self) -> PopStat:
        return PopStat(POP_START_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        enforce({POP_HUYO_ELAPSED: self._huyo_elapsed,
                 POP_RESHUFFLED: self._reshuffled}.get(stat.code), type(self.open))()

    def _huyo_elapsed(self) -> None:
        moderator.append(reshuffle_layer(delivery=self.delivery, hoyuusya=self.hoyuusya))

    def _reshuffled(self) -> None:
        if self.delivery.b_params.turn_count <= 2:
            moderator.pop()
            return
        for _ in range(2):
            self.delivery.hand_draw(hoyuusya=self.hoyuusya, is_mine=True)
        popup_message.add("カードを２枚引きます")
        moderator.pop()
