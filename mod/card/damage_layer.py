#                 20                  40                  60                 79
from typing import runtime_checkable, Protocol

from mod.const import UC_LIFE, opponent, enforce
from mod.classes import Card, Huda, Delivery, moderator
from mod.tf.taba_factory import TabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat
from mod.coous.damage_2_or_more import damage_2_or_more

@runtime_checkable
class _DamageArrow(Protocol):
    from_code: int
    to_code: int
    dmg: int

def _mouseup(huda: Huda) -> None:
    layer = moderator.last_layer()
    # da = enforce(huda.card, _DamageArrow)
    if not isinstance(da := huda.card, _DamageArrow):
        raise EOFError
    huda.delivery.send_ouka_to_ryouiki(hoyuusya=huda.hoyuusya, from_mine=False, from_code=da.from_code,
                                    to_mine=False, to_code=da.to_code, kazu=da.dmg)
    if da.dmg >= 2 and da.from_code == UC_LIFE:
        damage_2_or_more(delivery=huda.delivery, hoyuusya=opponent(huda.hoyuusya))
    if moderator.last_layer() == layer:
        moderator.pop()

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def damage_layer(card: Card, delivery: Delivery, hoyuusya: int, code: int) -> MonoChoiceLayer:
    # da = enforce(card, _DamageArrow)
    if not isinstance(da := card, _DamageArrow):
        raise EOFError
    mcl = MonoChoiceLayer(name=f"ダメージ解決：{da.from_code}から{da.to_code}へ{da.dmg}点", delivery=delivery, hoyuusya=hoyuusya,
                          moderate=_moderate, code=code)
    # mcl = MonoChoiceLayer(name=f"ダメージ解決", delivery=delivery, hoyuusya=hoyuusya,
    #                       moderate=_moderate, code=code)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=[card], delivery=delivery, hoyuusya=hoyuusya)
    return mcl
