#                 20                  40                  60                 79
from itertools import product

from mod.const import TC_SUTEHUDA, TC_KIRIHUDA, USAGE_DEPLOYED, UC_DUST,\
    USAGE_USED, POP_HUYO_ELAPSED
from mod.classes import Any, PopStat, Huda, Taba, Delivery, moderator
from mod.tf.taba_factory import TabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
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

# def layer(delivery: Delivery, hoyuusya: int, huda: Any | None=None, taba: Taba | None=None) -> PipelineLayer:
#     return PipelineLayer
