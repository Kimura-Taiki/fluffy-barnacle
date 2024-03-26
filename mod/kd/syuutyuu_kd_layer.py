#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Callable, Card, Huda, Delivery, moderator, popup_message
from mod.delivery import duck_delivery
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.kd.syuutyuu_mono_kd_layer import syuutyuu_mono_kd_layer
from mod.card.card_func import is_meet_conditions

_END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def can_syuutyuu(delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
    checks: list[tuple[bool, str]] = [
        (delivery.m_params(hoyuusya).played_zenryoku, "既に全力行動しています"),
        (delivery.m_params(hoyuusya).played_syuutan, "既に終端行動しています"),
        (delivery.b_params.phase_ended, "フェイズが終了しています"),
    ]
    return is_meet_conditions(checks=checks, popup=popup)

def syuutyuu_kd_layer(cards: list[Card], huda: Huda, code: int=POP_OK) -> PipelineLayer:
    delivery, hoyuusya = huda.delivery, huda.hoyuusya
    li = [card for card in cards if card.can_play(delivery, hoyuusya)]
    if not li:
        popup_message.add("選べる基本動作がありません")
        return _END_LAYER(code)
    if not can_syuutyuu(delivery, hoyuusya, True):
        return _END_LAYER(code)
    return PipelineLayer(name="集中を費やした基本動作", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=delivery,
    hoyuusya=hoyuusya, name="基本動作の選択", lower=li, code=POP_ACT1)),
POP_ACT1: lambda l, s: moderator.append(syuutyuu_mono_kd_layer(
    card=enforce(s.huda, Huda).card, huda=enforce(l.huda, Huda), code=POP_ACT2)),
POP_ACT2: lambda l, s: moderator.pop()
        }, huda=huda, code=code)
