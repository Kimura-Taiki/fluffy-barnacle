#                 20                  40                  60                 79
from mod.const import enforce, POP_END_PHASE_FINISHED, TC_TEHUDA, TC_HUSEHUDA,\
    POP_OK, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Callable, PopStat, Huda, Delivery, moderator,\
    popup_message
from mod.card.temp_koudou import TempKoudou, KoukaDI, auto_di
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    tehuda = enforce(layer.delivery.taba(hoyuusya=layer.hoyuusya,
        taba_code=TC_TEHUDA), list)
    moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
        hoyuusya, name="破棄手札の選択", lower=tehuda, code=code))

def _discard(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base,
                                        is_mine=True, taba_code=TC_HUSEHUDA)
    layer.moderate(PopStat(code=code))

def discard_layer(delivery: Delivery, hoyuusya: int, code: int=POP_OK)\
-> PipelineLayer:
    return PipelineLayer(name="手札を１枚伏せる",
    delivery=delivery, hoyuusya=hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _open(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _discard(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }, code=code)

discard: KoukaDI = lambda delivery, hoyuusya: moderator.append(discard_layer(
    delivery=delivery, hoyuusya=hoyuusya, code=POP_OK))

discard_card = TempKoudou(name="手札を１枚伏せる", cond=auto_di, kouka=discard)
