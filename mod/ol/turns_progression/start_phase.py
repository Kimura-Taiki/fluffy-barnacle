#                 20                  40                  60                 79
from mod.const import POP_START_PHASE_FINISHED, POP_OPEN, POP_HUYO_ELAPSED,\
    POP_RESHUFFLED, UC_ZYOGAI, UC_SYUUTYUU, side_name, SIMOTE, KAMITE
from mod.classes import Callable, PopStat, Delivery, moderator, popup_message
from mod.ol.remove_osame.remove_osame import RemoveOsame
from mod.ol.reshuffle import reshuffle_layer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    popup_message.add(f"{side_name(layer.hoyuusya)}のターンです")
    layer.delivery.b_params.start_turn()
    layer.delivery.m_params(hoyuusya=SIMOTE).start_turn()
    layer.delivery.m_params(hoyuusya=KAMITE).start_turn()
    layer.delivery.send_ouka_to_ryouiki(
        hoyuusya=layer.hoyuusya, from_mine=False, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU)
    popup_message.add("集中力を１得ます")
    moderator.append(RemoveOsame(delivery=layer.delivery, hoyuusya=layer.hoyuusya))

def _huyo_elapsed(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.append(reshuffle_layer(delivery=layer.delivery, hoyuusya=layer.hoyuusya))

def _reshuffled(layer: PipelineLayer,  stat: PopStat) -> None:
    if layer.delivery.b_params.turn_count <= 2:
        moderator.pop()
        return
    for _ in range(2):
        layer.delivery.hand_draw(hoyuusya=layer.hoyuusya, is_mine=True)
    popup_message.add("カードを２枚引きます")
    moderator.pop()

start_phase_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="開始フェイズ", delivery=delivery, gotoes={
        POP_OPEN: _open,
        POP_HUYO_ELAPSED: _huyo_elapsed,
        POP_RESHUFFLED: _reshuffled
    }, code=POP_START_PHASE_FINISHED)
