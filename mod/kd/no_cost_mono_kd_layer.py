#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import PopStat, Card, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer
from mod.kd.share import END_LAYER, can_kd

def _kaiketu(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    enforce(layer.card, Card).kaiketu(layer.delivery, layer.hoyuusya, code=code)

def _no_cost(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.moderate(PopStat(code))

def no_cost_mono_kd_layer(card: Card, delivery: Delivery, hoyuusya: int, code: int=POP_OK) -> PipelineLayer:
    if not can_kd(delivery, hoyuusya, True):
        return END_LAYER(code)
    return PipelineLayer(name=f"基本動作「{card.name}」", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _kaiketu(l, s, POP_ACT1),
POP_ACT1: lambda l, s: _no_cost(l, s, POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop(),
        }, card=card, code=code)
