#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3,\
    SC_MODULO, TG_KOUDOU_KAIKETUED
from mod.classes import Any, PopStat, Card, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer
from mod.coous.trigger import Trigger, auto_diic, solve_trigger_effect
from mod.coous.scalar_correction import applied_scalar
from mod.kd.kihondousa import kd_list
from mod.kd.no_cost_kd_layer import no_cost_kd_layer
from mod.card.temp_koudou import TempKoudou, auto_di

def _kouka_modulo(delivery :Delivery, hoyuusya: int) -> None:
    li = [enforce(card, Card) for card in kd_list]
    moderator.append(no_cost_kd_layer(li, delivery, hoyuusya))

_modulo = TempKoudou("もじゅろー効果", auto_di, kouka=_kouka_modulo)

def _memo_modulo(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    print("Memo Modulo")
    if applied_scalar(i=0, scalar=SC_MODULO, delivery=layer.delivery, hoyuusya=layer.hoyuusya):
        layer.delivery.m_params(layer.hoyuusya).lingerings.append(
            Trigger("予約効果：もじゅろー", auto_diic, TG_KOUDOU_KAIKETUED, _modulo, True))
    layer.moderate(PopStat(code))

def _kouka(layer: PipelineLayer, stat: PopStat) -> None:
    enforce(layer.card, Card).kouka(layer.delivery, layer.hoyuusya)
    if moderator.last_layer() == layer:
        moderator.pop()

def _kaiketu(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    enforce(layer.card, Card).kouka(layer.delivery, layer.hoyuusya)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code))

def _trigger_modulo(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    solve_trigger_effect(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                         trigger=TG_KOUDOU_KAIKETUED, code=code)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code))

def play_koudou_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"行動:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _memo_modulo(l, s, POP_ACT1),
POP_ACT1: lambda l, s: _kaiketu(l, s, POP_ACT2),
POP_OK: lambda l, s: l.moderate(PopStat(POP_ACT2)),
POP_ACT2: lambda l, s: _trigger_modulo(l, s, POP_ACT3),
POP_ACT3: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)

def play_div_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"効果:{card.name}を解決", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _kouka,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)
