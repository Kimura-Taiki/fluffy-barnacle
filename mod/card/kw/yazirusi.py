#                 20                  40                  60                 79
from typing import NamedTuple, Any

from mod.const import UC_DUST, UC_MAAI, UC_ZYOGAI, UC_SYUUTYUU, UC_ISYUKU
from mod.delivery import Delivery

class Yazirusi(NamedTuple):
    from_mine: bool = False
    from_code: int = UC_DUST
    to_mine: bool = False
    to_code: int = UC_DUST
    kazu: int = 1

    def send(self, delivery: Delivery, hoyuusya: int) -> None:
        self.finally_send(delivery=delivery, hoyuusya=hoyuusya)

    def finally_send(self, delivery: Delivery, hoyuusya: int) -> None:
        delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya,
            from_mine=self.from_mine, from_code=self.from_code,
            to_mine=self.to_mine, to_code=self.to_code, kazu=self.kazu)
        
    def listed(self) -> list[Any]:
        return [self.from_mine, self.from_code,
                self.to_mine, self.to_code, self.kazu]

ya_moguri = Yazirusi(from_code=UC_MAAI)
ya_ridatu = Yazirusi(to_code=UC_MAAI)
