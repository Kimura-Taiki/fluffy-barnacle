#                 20                  40                  60                 79
from mod.const import enforce, POP_END_PHASE_FINISHED, POP_END_TRIGGERED,\
    POP_DISCARDED, TG_END_PHASE, TC_TEHUDA, TC_HUSEHUDA, POP_OPEN
from mod.classes import Callable, PopStat, Huda, Delivery, moderator, popup_message
from mod.coous.trigger import solve_trigger_effect
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    solve_trigger_effect(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                         trigger=TG_END_PHASE, code=POP_END_TRIGGERED)
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code=POP_END_TRIGGERED))

def _end_triggered(layer: PipelineLayer, stat: PopStat) -> None:
    _check_discard(layer=layer)

def _discarded(layer: PipelineLayer, stat: PopStat) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_HUSEHUDA)
    _check_discard(layer=layer)

def _check_discard(layer: PipelineLayer) -> None:
    tehuda = enforce(layer.delivery.taba_target(hoyuusya=layer.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), list)
    if len(tehuda) <= layer.delivery.b_params.tehuda_max:
        popup_message.add("ターンを終了します")
        moderator.pop()
        return
    moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
        hoyuusya, name="超過手札の破棄", lower=tehuda, code=POP_DISCARDED))

end_phase_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="終了フェイズ", delivery=delivery, gotoes={
        POP_OPEN: _open,
        POP_END_TRIGGERED: _end_triggered,
        POP_DISCARDED: _discarded
    }, code=POP_END_PHASE_FINISHED)
