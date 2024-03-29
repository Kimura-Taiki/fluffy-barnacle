#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Card, Huda, Delivery, moderator, popup_message
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.kd.no_cost_mono_kd_layer import no_cost_mono_kd_layer
from mod.card.card_func import is_meet_conditions
from mod.kd.share import END_LAYER

def _can_kd(delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
    checks: list[tuple[bool, str]] = [
        (delivery.m_params(hoyuusya).played_zenryoku, "既に全力行動しています"),
        (delivery.m_params(hoyuusya).played_syuutan, "既に終端行動しています"),
        (delivery.b_params.phase_ended, "フェイズが終了しています"),
    ]
    return is_meet_conditions(checks=checks, popup=popup)

def no_cost_kd_layer(cards: list[Card], delivery: Delivery, hoyuusya: int, code: int=POP_OK) -> PipelineLayer:
    li = [card for card in cards if card.can_play(delivery, hoyuusya)]
    if not li:
        popup_message.add("選べる基本動作がありません")
        return END_LAYER(code)
    if not _can_kd(delivery, hoyuusya, True):
        return END_LAYER(code)
    return PipelineLayer(name="集中を費やした基本動作", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=delivery,
    hoyuusya=hoyuusya, name="基本動作の選択", lower=li, code=POP_ACT1)),
POP_ACT1: lambda l, s: moderator.append(no_cost_mono_kd_layer(
    card=enforce(s.huda, Huda).card, delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT2)),
POP_ACT2: lambda l, s: moderator.pop()
        }, code=code)
