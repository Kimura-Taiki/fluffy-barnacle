#                 20                  40                  60                 79
from mod.const import TC_TEHUDA, TC_KIRIHUDA, POP_TAIOUED, side_name, OBAL_USE_CARD
from mod.classes import Card, Huda, Taba, Delivery, TabaFactory, Callable, popup_message
from mod.ol.others_basic_action import obal_func

def taiou_taba(delivery: Delivery, hoyuusya: int, kougeki: Card) -> Taba:
    return _taiou_factory(mouseup=_taiou_mouseup).maid_by_hudas(
        hudas=_taiou_hudas(delivery=delivery, hoyuusya=hoyuusya, kougeki=kougeki), hoyuusya=hoyuusya)

def _taiou_hudas(delivery: Delivery, hoyuusya: int, kougeki: Card) -> list[Huda]:
    return [
        huda
        for taba_code in [TC_TEHUDA, TC_KIRIHUDA]
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=False, taba_code=taba_code), Taba)
        for huda in taba
        if huda.card.taiou and huda.can_play() and kougeki.nontaiouble(delivery, hoyuusya, huda.card) 
        ]

def _taiou_factory(mouseup: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={"mouseup": mouseup}, is_ol=True)

def _taiou_mouseup(huda: Huda) -> None:
    huda.delivery.b_params.during_taiou = True
    obal_func(cards=[huda.card], name=f"{side_name(huda.hoyuusya)}の対応「{huda.card.name}」の使用", text=f"{side_name(huda.hoyuusya)}は対応して「{huda.card.name}」カードを使います",
              mode=OBAL_USE_CARD, code=POP_TAIOUED)(huda)
    # popup_message.add(f"{side_name(huda.hoyuusya)}は対応して「{huda.card.name}」カードを使います")
    # huda.card.kaiketu(delivery=huda.delivery, hoyuusya=huda.hoyuusya, huda=huda.base, code=POP_TAIOUED)
