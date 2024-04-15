#                 20                  40                  60                 79
from typing import runtime_checkable, Protocol

from mod.const import UC_AURA, UC_LIFE, opponent, TG_1_OR_MORE_DAMAGE,\
    TG_2_OR_MORE_DAMAGE, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3
from mod.classes import Any, Card, Delivery, moderator
from mod.ol.pop_stat import PopStat
from mod.coous.trigger import solve_trigger_effect
from mod.ol.pipeline_layer import PipelineLayer
from mod.coous.aura_guard import huyo_aura_guard, aura_guard_huda
from mod.card.distribute_layer import distribute_layer

@runtime_checkable
class _DamageArrow(Protocol):
    from_code: int
    to_code: int
    dmg: int
    attr: int

def _huyo_ukeable(da: _DamageArrow, delivery: Delivery, hoyuusya: int) -> bool:
    return da.from_code == UC_AURA and huyo_aura_guard(delivery=delivery, hoyuusya=hoyuusya) > 0

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    da = _enforce_da(layer.card)
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    if _huyo_ukeable(da=da, delivery=delivery, hoyuusya=opponent(hoyuusya)):
        moderator.append(distribute_layer(dmg=da.dmg, delivery=delivery, hoyuusya=opponent(hoyuusya),
            huda=aura_guard_huda(delivery=delivery, hoyuusya=opponent(hoyuusya)), code=code))
    else:
        layer.delivery.send_ouka_to_ryouiki(hoyuusya=layer.hoyuusya, from_mine=
            False, from_code=da.from_code, to_mine=False, to_code=da.to_code,
            kazu=da.dmg)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code, stat.huda))

def _damaged1(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    da = _enforce_da(layer.card)
    layer.delivery.b_params.damage_attr = da.attr
    if da.dmg >= 1 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=layer.delivery, hoyuusya=opponent(layer.
            hoyuusya), trigger=TG_1_OR_MORE_DAMAGE, code=code)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code, stat.huda))

def _damaged2(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    da = _enforce_da(layer.card)
    if da.dmg >= 1 and da.from_code == UC_AURA:
        layer.delivery.m_params(opponent(layer.hoyuusya)).aura_damaged = True
    if da.dmg >= 2 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=layer.delivery, hoyuusya=opponent(layer.
            hoyuusya), trigger=TG_2_OR_MORE_DAMAGE, code=code)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code))

def _damaged3(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.pop()

def _enforce_da(card: Any) -> _DamageArrow:
    if not isinstance(card, _DamageArrow):
        raise ValueError("Damageではありません")
    return card

def damage_layer(card: Card, delivery: Delivery, hoyuusya: int, code: int) ->\
PipelineLayer:
    da = _enforce_da(card)
    return PipelineLayer(name=f"ダメージ解決：{da.from_code}から{da.to_code}へ\
        {da.dmg}点", delivery=delivery, hoyuusya=hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _open(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _damaged1(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _damaged2(l, s, POP_ACT3),
        POP_ACT3: _damaged3,
    }, card=card, code=code)
