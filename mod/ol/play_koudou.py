#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN
from mod.classes import Any, PopStat, Card, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    enforce(layer.card, Card).kouka(layer.delivery, layer.hoyuusya)
    if moderator.last_layer() == layer:
        moderator.pop()

def play_koudou_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"行動:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _open,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)

def play_div_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"効果:{card.name}を解決", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _open,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)
