#                 20                  40                  60                 79
from itertools import product

from mod.const import TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, UC_DUST,\
    USAGE_USED, POP_HUYO_ELAPSED, POP_OK, POP_OPEN, POP_CHOICED,\
    POP_KAIKETUED, enforce
from mod.classes import Any, PopStat, Card, Huda, Taba, Delivery, moderator
from mod.tf.taba_factory import TabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

def huyo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    return [
        huda
        for is_mine, taba_code in product([False, True], [TC_SUTEHUDA, TC_KIRIHUDA])
        if isinstance(taba := delivery.taba_target(hoyuusya=hoyuusya, is_mine=is_mine, taba_code=taba_code), Taba)
        for huda in taba
        if huda.usage == USAGE_DEPLOYED
    ]

def _mouseup(huda: Huda) -> None:
    base = huda.base
    base.delivery.send_ouka_to_ryouiki(hoyuusya=base.hoyuusya, from_huda=base, to_mine=False, to_code=UC_DUST)
    huda.withdraw()
    if base.osame == 0:
        base.usage = USAGE_USED
        if huda.card.hakizi:
            huda.card.hakizi.kaiketu(delivery=huda.delivery, hoyuusya=huda.hoyuusya)
            return
    moderator.last_layer().moderate(PopStat())

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def single_remove_layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None, taba: Taba | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(
        name="償却する付与の選択", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
        moderate=_moderate, code=POP_HUYO_ELAPSED)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    hudas: list[Huda] = (
        huyo_hudas(delivery=delivery, hoyuusya=hoyuusya)
        if taba is None
        else [proxy.base for proxy in taba])
    mcl.taba = factory.maid_by_hudas(hudas=hudas, hoyuusya=hoyuusya)
    return mcl

def _amortize_huyo(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if not stat.huda:
        moderator.pop()
        return
    huda = enforce(stat.huda, Huda)
    base = huda.base

    print(base.card.name, base.osame, base)
    base.delivery.send_ouka_to_ryouiki(hoyuusya=base.hoyuusya, from_huda=base)
    print(base.card.name, base.osame, base)
    # rest = stat.rest_taba
    # rest.remove(huda)
    layer.rest = [enforce(huda, Huda).base for huda in stat.rest_taba]
    if base.osame == 0:
        base.usage = USAGE_USED
        if base.card.hakizi:
            base.card.hakizi.kaiketu(delivery=base.delivery, hoyuusya=base.
                                     hoyuusya, code=code)
            return
    layer.moderate(PopStat(code=code))

#                 20                  40                  60                 79
def choice_layer(hudas: list[Huda], delivery: Delivery, hoyuusya: int,
    code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name="OsameAllocation", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=
            delivery, hoyuusya=hoyuusya, name="償却する付与の選択", lower=hudas,
            code=POP_CHOICED)),
        POP_CHOICED: lambda l, s,: _amortize_huyo(l, s, POP_KAIKETUED),
        POP_KAIKETUED: lambda l, s: moderator.pop()
    }, code=code)
# def layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None, taba: Taba | None=None) -> PipelineLayer:
#     return PipelineLayer
