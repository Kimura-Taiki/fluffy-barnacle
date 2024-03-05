#                 20                  40                  60                 79
from mod.const import TC_TEHUDA, TC_KIRIHUDA
from mod.classes import Card, Huda, Taba, Delivery

def taiou_hudas(card: Card, delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for taba_code in [TC_TEHUDA, TC_KIRIHUDA]
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=taba_code), Taba)
        for huda in taba
        if huda.card.taiou and huda.can_play() and card.nontaiouble(delivery, hoyuusya, huda.card) 
        ]
