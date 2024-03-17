#                 20                  40                  60                 79
from mod.const import enforce, POP_END_PHASE_FINISHED, POP_END_TRIGGERED,\
    POP_DISCARDED, TG_END_PHASE, TC_TEHUDA, TC_HUSEHUDA, POP_OPEN, POP_ACT1,\
    POP_ACT2, POP_ACT3
from mod.classes import Callable, PopStat, Huda, Delivery, moderator, popup_message
from mod.coous.trigger import solve_trigger_effect
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.discard import discard_layer

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    solve_trigger_effect(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                         trigger=TG_END_PHASE, code=code)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code=code))

def 

def _check_discard(layer: PipelineLayer, stat: PopStat, discard_code: int,
                   end_code: int) -> None:
    tehuda = enforce(layer.delivery.taba(hoyuusya=layer.hoyuusya, taba_code=TC_TEHUDA), list)
    if len(tehuda) > layer.delivery.b_params.tehuda_max:
        moderator.append(discard_layer(layer.delivery, layer.hoyuusya, code=discard_code))
    else:
        layer.moderate(PopStat(end_code))

def _end(layer: PipelineLayer, stat: PopStat) -> None:
    popup_message.add("ターンを終了します")
    moderator.pop()

end_phase_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="終了フェイズ", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: _open(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _kasa_kaihei(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _check_discard(l, s, POP_ACT2, POP_ACT3),
        POP_ACT3: _end
    }, code=POP_END_PHASE_FINISHED)
