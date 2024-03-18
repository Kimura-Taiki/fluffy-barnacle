#                 20                  40                  60                 79
from typing import NamedTuple, Any

from mod.const import UC_DUST, UC_MAAI, UC_AURA, UC_ZYOGAI, UC_SYUUTYUU, UC_ISYUKU,\
    SC_SMOKE, SC_UROUO_YAZIRUSI, POP_OPEN, POP_ACT1
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.coous.scalar_correction import applied_scalar
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat
from mod.ol.choice import choice_layer
from mod.ol.pipeline_layer import PipelineLayer

class Yazirusi(NamedTuple):
    from_mine: bool = False
    from_code: int = UC_DUST
    to_mine: bool = False
    to_code: int = UC_DUST
    kazu: int = 1

    def send(self, delivery: Delivery, hoyuusya: int) -> None:
        if applied_scalar(i=0, scalar=SC_UROUO_YAZIRUSI, delivery=delivery, hoyuusya=hoyuusya) > 0:
            self.each_send(delivery, hoyuusya)
        else:
            self.finally_send(delivery=delivery, hoyuusya=hoyuusya)

    def each_send(self, delivery: Delivery, hoyuusya: int) -> None:
        from mod.card.temp_koudou import TempKoudou, auto_di
        reverse_yazirusi = Yazirusi(self.to_mine, self.to_code, self.from_mine, self.from_code, self.kazu)
        forward_card = TempKoudou("正処理", auto_di, yazirusi=self)
        forward_card.kouka = self.finally_send
        reverse_card = TempKoudou("逆処理", auto_di, yazirusi=reverse_yazirusi)
        reverse_card.kouka = reverse_yazirusi.finally_send
        moderator.append(choice_layer(cards=[forward_card, reverse_card], delivery=delivery, hoyuusya=hoyuusya))

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
ya_matoi = Yazirusi(to_mine=True, to_code=UC_AURA)