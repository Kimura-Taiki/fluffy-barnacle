#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3,\
    SC_MODULO, TG_KOUDOU_KAIKETUED
from mod.classes import Any, PopStat, Card, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer
from mod.coous.trigger import Trigger, auto_diic
from mod.coous.scalar_correction import applied_scalar
from mod.kd.kihondousa import kd_list

# def _modulo_cmd(delivery :Delivery, hoyuusya: int) -> None:
    

# def _memo_modulo(layer: PipelineLayer, stat: PopStat) -> None:
#     if applied_scalar(i=0, scalar=SC_MODULO, delivery=layer.delivery, hoyuusya=layer.hoyuusya):
#         layer.delivery.m_params(layer.hoyuusya).lingerings.append(Trigger("予約効果：もじゅろー", auto_diic, TG_KOUDOU_KAIKETUED))

def _kouka(layer: PipelineLayer, stat: PopStat) -> None:
    enforce(layer.card, Card).kouka(layer.delivery, layer.hoyuusya)
    if moderator.last_layer() == layer:
        moderator.pop()

def play_koudou_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"行動:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _kouka,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)

def play_div_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"効果:{card.name}を解決", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _kouka,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)
