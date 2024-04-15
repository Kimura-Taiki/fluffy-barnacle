#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_CHOICED, POP_KAIKETUED
from mod.classes import PopStat, Card, Huda, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

def _kaiketued(layer: PipelineLayer, stat: PopStat) -> None:
    layer.huda, layer.card = stat.huda, stat.card
    moderator.pop()

def choice_layer(cards: list[Card], delivery: Delivery, hoyuusya: int,
huda: Huda | None=None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name="ChoiceLayer", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=
            delivery, hoyuusya=hoyuusya, name="効果の選択", lower=cards,
            code=POP_CHOICED)),
        POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=
            delivery, hoyuusya=hoyuusya, huda=huda, code=POP_KAIKETUED),
        POP_KAIKETUED: lambda l, s: _kaiketued(l, s)
        # POP_KAIKETUED: lambda l, s: moderator.pop()
    }, huda=huda, code=code)
