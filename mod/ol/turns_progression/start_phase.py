#                 20                  40                  60                 79
from mod.const import POP_START_PHASE_FINISHED, POP_OPEN, POP_HUYO_ELAPSED,\
    POP_RESHUFFLED, POP_TURN_DRAWED, UC_ZYOGAI, UC_SYUUTYUU, SIMOTE, KAMITE,\
    UC_ISYUKU, side_name
from mod.classes import Callable, PopStat, Delivery, moderator, popup_message
from mod.ol.remove_osame.remove_osame import RemoveOsame
from mod.ol.reshuffle import reshuffle_layer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer
from mod.ol.turns_progression.turn_draw import turn_draw_layer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    popup_message.add(f"{side_name(layer.hoyuusya)}のターンです")
    layer.delivery.b_params.start_turn()
    layer.delivery.m_params(hoyuusya=SIMOTE).start_turn()
    layer.delivery.m_params(hoyuusya=KAMITE).start_turn()
    _add_syuutyuu(layer=layer)
    moderator.append(RemoveOsame(delivery=layer.delivery, hoyuusya=layer.hoyuusya))

def _add_syuutyuu(layer: PipelineLayer) -> None:
    if layer.delivery.ouka_count(hoyuusya=layer.hoyuusya, is_mine=True,
                                 utuwa_code=UC_ISYUKU) > 0:
        popup_message.add("畏縮を解除します")
        layer.delivery.send_ouka_to_ryouiki(hoyuusya=layer.hoyuusya, from_mine=
            True, from_code=UC_ISYUKU, to_code=UC_ZYOGAI)
    else:
        popup_message.add("集中力を１得ます")
        layer.delivery.send_ouka_to_ryouiki(
            hoyuusya=layer.hoyuusya, from_mine=False, from_code=UC_ZYOGAI,
            to_mine=True, to_code=UC_SYUUTYUU)

def _huyo_elapsed(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.append(reshuffle_layer(delivery=layer.delivery, hoyuusya=layer.hoyuusya))

def _reshuffled(layer: PipelineLayer,  stat: PopStat) -> None:
    if layer.delivery.b_params.turn_count <= 2:
        moderator.pop()
        return
    moderator.append(turn_draw_layer(layer.delivery))

def _turn_drawed(layer: PipelineLayer,  stat: PopStat) -> None:
    moderator.pop()

start_phase_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="開始フェイズ", delivery=delivery, gotoes={
        POP_OPEN: _open,
        POP_HUYO_ELAPSED: _huyo_elapsed,
        POP_RESHUFFLED: _reshuffled,
        POP_TURN_DRAWED: _turn_drawed
    }, code=POP_START_PHASE_FINISHED)
