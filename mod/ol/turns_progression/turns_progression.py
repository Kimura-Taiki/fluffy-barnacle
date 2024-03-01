#                 20                  40                  60                 79
from mod.const import opponent, side_name, POP_OPEN, POP_START_PHASE_FINISHED,\
    POP_MAIN_PHASE_FINISHED, POP_END_PHASE_FINISHED, SIMOTE
from mod.classes import Callable, Delivery, PopStat, moderator
from mod.ol.turns_progression.start_phase import start_phase_layer
from mod.ol.turns_progression.main_phase import MainPhase
from mod.ol.turns_progression.end_phase import end_phase_layer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.append(MainPhase(inject_func=layer.inject_func))
    layer.delivery.b_params.turn_count = 1
    layer.delivery.turn_player = SIMOTE
    print(f"ターンプレイヤーを{side_name(layer.delivery.turn_player)}にしたよ")
    layer.name = _layer_name(delivery=layer.delivery)

def _start_phase_finished(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.append(MainPhase(delivery=layer.delivery, inject_func=layer.inject_func))

def _main_phase_finished(layer: PipelineLayer, stat: PopStat) -> None:
    moderator.append(end_phase_layer(layer.delivery))

def _end_phase_finished(layer: PipelineLayer, stat: PopStat) -> None:
    layer.delivery.b_params.turn_count += 1
    layer.delivery.turn_player = opponent(layer.delivery.turn_player)
    layer.name = _layer_name(delivery=layer.delivery)
    moderator.append(start_phase_layer(layer.delivery))

def _layer_name(delivery: Delivery) -> str:
    return f"{delivery.b_params.turn_count}ターン目 {side_name(delivery.turn_player)}"

def turns_progression_layer(delivery: Delivery, inject_func: Callable[[], None]) -> PipelineLayer:
    layer = PipelineLayer(name="終了フェイズ", delivery=delivery, gotoes={
        POP_OPEN: _open,
        POP_START_PHASE_FINISHED: _start_phase_finished,
        POP_MAIN_PHASE_FINISHED: _main_phase_finished,
        POP_END_PHASE_FINISHED: _end_phase_finished
    }, code=POP_END_PHASE_FINISHED)
    layer.inject_func = inject_func
    return layer
