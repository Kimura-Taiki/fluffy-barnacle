#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2,\
    TC_HUSEHUDA
from mod.classes import Callable, PopStat, Card, Huda, moderator
from mod.delivery import duck_delivery
from mod.ol.pipeline_layer import PipelineLayer

_END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def _kaiketu(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    enforce(layer.card, Card).kaiketu(layer.delivery, layer.hoyuusya,
        huda=enforce(layer.huda, Huda), code=code)

def _husecard(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    print("kaiketu", stat, stat.huda.card.name if stat.huda else None, stat.card.name if stat.card else None)
    layer.delivery.m_params(layer.hoyuusya).played_standard = True
    huda = enforce(layer.huda, Huda)
    layer.delivery.send_huda_to_ryouiki(huda=huda.base, is_mine=True,
        taba_code=TC_HUSEHUDA)
    moderator.pop()

def hand_mono_kd_layer(card: Card, huda: Huda, code: int=POP_OK) -> PipelineLayer:
    delivery, hoyuusya = huda.delivery, huda.hoyuusya
    if not card.can_play(delivery, hoyuusya, True):
        return _END_LAYER(code)
    if not huda.can_standard(True, False):
        return _END_LAYER(code)
    return PipelineLayer(name=f"手札基本動作「{card.name}」", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _kaiketu(l, s, POP_ACT1),
POP_ACT1: lambda l, s: _husecard(l, s, POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop(),
        },huda=huda, card=card, code=code)
