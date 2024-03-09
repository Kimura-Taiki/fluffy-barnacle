#                 20                  40                  60                 79
from itertools import product

from mod.const import TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, USAGE_USED,\
    POP_OK, POP_OPEN, POP_CHOICED, POP_ACT1, POP_KAIKETUED, enforce
from mod.classes import PopStat, Huda, Taba, Delivery, moderator
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer

def huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True],
                                          [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(
            hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _amortize_huyo(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if not stat.huda:
        moderator.pop()
        return
    huda = enforce(stat.huda, Huda)
    base = huda.base
    layer.huda = base
    layer.rest = [enforce(huda, Huda).base for huda in stat.rest_taba]
    base.card.amortize(base)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code=code))

def _hakizi(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    huda = enforce(layer.huda, Huda)
    if huda.osame == 0:
        huda.usage = USAGE_USED
        if huda.card.hakizi:
            huda.card.hakizi.kaiketu(delivery=huda.delivery, hoyuusya=huda.
                                     hoyuusya, code=code)
            return
    layer.moderate(PopStat(code=code))


def single_remove_layer(hudas: list[Huda], delivery: Delivery, hoyuusya: int,
    code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name="OsameAllocation", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=
            delivery, hoyuusya=hoyuusya, name="償却する付与の選択", lower=hudas,
            code=POP_CHOICED)),
        POP_CHOICED: lambda l, s,: _amortize_huyo(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _hakizi(l, s, POP_KAIKETUED),
        POP_KAIKETUED: lambda l, s: moderator.pop()
    }, code=code)
