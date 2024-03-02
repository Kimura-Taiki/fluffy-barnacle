#                 20                  40                  60                 79
from typing import runtime_checkable, Protocol

from mod.const import UC_LIFE, opponent, TG_1_OR_MORE_DAMAGE,\
    TG_2_OR_MORE_DAMAGE, POP_OPEN, POP_DAMAGED_1, POP_DAMAGED_2
from mod.classes import Any, Card, Delivery, moderator
from mod.ol.pop_stat import PopStat
from mod.coous.trigger import solve_trigger_effect
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

@runtime_checkable
class _DamageArrow(Protocol):
    from_code: int
    to_code: int
    dmg: int
    attr: int

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    da = _enforce_da(layer.card)
    layer.delivery.send_ouka_to_ryouiki(hoyuusya=layer.hoyuusya, from_mine=
        False, from_code=da.from_code, to_mine=False, to_code=da.to_code,
        kazu=da.dmg)
    layer.delivery.b_params.damage_attr = da.attr
    if da.dmg >= 1 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=layer.delivery, hoyuusya=opponent(layer.
            hoyuusya), trigger=TG_1_OR_MORE_DAMAGE, code=POP_DAMAGED_1)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(POP_DAMAGED_1, stat.huda))

def _damaged1(layer: PipelineLayer, stat: PopStat) -> None:
    da = _enforce_da(layer.card)
    if da.dmg >= 2 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=layer.delivery, hoyuusya=opponent(layer.
            hoyuusya), trigger=TG_2_OR_MORE_DAMAGE, code=POP_DAMAGED_2)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(POP_DAMAGED_2))

def _damaged2(layer: PipelineLayer, stat: PopStat) -> None:
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
        POP_OPEN: _open,
        POP_DAMAGED_1: _damaged1,
        POP_DAMAGED_2: _damaged2,
    }, card=card, code=code)
