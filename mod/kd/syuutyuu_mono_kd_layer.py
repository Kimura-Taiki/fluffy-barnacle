#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Callable, PopStat, Card, Huda, Delivery, moderator
from mod.delivery import duck_delivery
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.syuutyuu import reduce_syuutyuu
from mod.card.card_func import is_meet_conditions
from mod.kd.share import END_LAYER

def can_syuutyuu(delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
    checks: list[tuple[bool, str]] = [
        (delivery.m_params(hoyuusya).played_zenryoku, "既に全力行動しています"),
        (delivery.m_params(hoyuusya).played_syuutan, "既に終端行動しています"),
        (delivery.b_params.phase_ended, "フェイズが終了しています"),
    ]
    return is_meet_conditions(checks=checks, popup=popup)

def _kaiketu(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    enforce(layer.card, Card).kaiketu(layer.delivery, layer.hoyuusya, code=code)

def _reduce(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    reduce_syuutyuu(layer.delivery, layer.hoyuusya)
    layer.moderate(PopStat(code))

def syuutyuu_mono_kd_layer(card: Card, delivery: Delivery, hoyuusya: int, code: int=POP_OK) -> PipelineLayer:
    if not can_syuutyuu(delivery, hoyuusya, True):
        return END_LAYER(code)
    return PipelineLayer(name=f"集中基本動作「{card.name}」", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _kaiketu(l, s, POP_ACT1),
POP_ACT1: lambda l, s: _reduce(l, s, POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop(),
        }, card=card, code=code)
