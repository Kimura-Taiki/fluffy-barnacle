#                 20                  40                  60                 79
from typing import NamedTuple, Any

from mod.const import UC_DUST, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, UC_ISYUKU,\
    SC_SMOKE
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.coous.scalar_correction import applied_scalar
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat

class Yazirusi(NamedTuple):
    from_mine: bool = False
    from_code: int = UC_DUST
    to_mine: bool = False
    to_code: int = UC_DUST
    kazu: int = 1

    def send(self, delivery: Delivery, hoyuusya: int) -> None:
        self.finally_send(delivery=delivery, hoyuusya=hoyuusya)

    def finally_send(self, delivery: Delivery, hoyuusya: int)-> None:
        layer = moderator.last_layer()
        if applied_scalar(i=0, scalar=SC_SMOKE, delivery=delivery) > 0 and\
        self.from_code == UC_MAAI:
            popup_message.add("スモーク中に矢印効果で間合の桜花結晶は剥がせません")
        else:
            delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya,
                from_mine=self.from_mine, from_code=self.from_code,
                to_mine=self.to_mine, to_code=self.to_code, kazu=self.kazu)

    def listed(self) -> list[Any]:
        return [self.from_mine, self.from_code,
                self.to_mine, self.to_code, self.kazu]

ya_moguri = Yazirusi(from_code=UC_MAAI)
ya_ridatu = Yazirusi(to_code=UC_MAAI)
