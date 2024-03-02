#                 20                  40                  60                 79
from typing import Any

from mod.const import enforce, POP_OPEN, POP_CHOICED, POP_KAIKETUED
from mod.classes import Card, Huda, Delivery, moderator
from mod.ol.turns_progression.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

def choice_layer(cards: list[Card], delivery: Delivery, hoyuusya: int, huda:
Any | None=None) -> PipelineLayer:
    return PipelineLayer(name="ChoiceLayer", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=
            delivery, hoyuusya=hoyuusya, name="効果の選択", lower=cards,
            code=POP_CHOICED)),
        POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=
            delivery, hoyuusya=hoyuusya, code=POP_KAIKETUED),
        POP_KAIKETUED: lambda l, s: moderator.pop()
    })
