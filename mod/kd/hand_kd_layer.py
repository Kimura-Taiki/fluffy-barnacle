#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Callable, Card, Huda, moderator, popup_message
from mod.delivery import duck_delivery
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.kd.hand_mono_kd_layer import hand_mono_kd_layer
from mod.kd.share import END_LAYER

def hand_kd_layer(cards: list[Card], huda: Huda, code: int=POP_OK) -> PipelineLayer:
    delivery, hoyuusya = huda.delivery, huda.hoyuusya
    li = [card for card in cards if card.can_play(delivery, hoyuusya)]
    if not li:
        popup_message.add("選べる基本動作がありません")
        return END_LAYER(code)
    if not huda.can_standard(True, False):
        return END_LAYER(code)
    return PipelineLayer(name="手札を費やした基本動作", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=delivery,
    hoyuusya=hoyuusya, name="基本動作の選択", lower=li, code=POP_ACT1)),
POP_ACT1: lambda l, s: moderator.append(hand_mono_kd_layer(
    card=enforce(s.huda, Huda).card, huda=enforce(l.huda, Huda), code=POP_ACT2)),
POP_ACT2: lambda l, s: moderator.pop()
        }, huda=huda, code=code)
