from typing import Callable

from mod.const import enforce, TC_KIRIHUDA, USAGE_USED, USAGE_UNUSED
from mod.delivery import Delivery
from mod.taba import Taba
from mod.popup_message import popup_message

def saiki_kouka(card_name: str) -> Callable[[Delivery, int], None]:
    def func(delivery: Delivery, hoyuusya: int) -> None:
        if not (huda := next((huda for huda in enforce(
            delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA),
            Taba) if huda.card.name == card_name), None)):
            popup_message.add(f"切り札「{card_name}」が見つかりませんでした")
            return
        if huda.usage != USAGE_USED:
            return
        huda.usage = USAGE_UNUSED
        popup_message.add(f"切り札「{card_name}」が再起しました")
    return func
