#                 20                  40                  60                 79
from mod.const import POP_OPEN, POP_TURN_DRAWED, POP_ACT1
from mod.classes import Callable, PopStat, Delivery, moderator, popup_message
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.handraw import handraw_layer

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    popup_message.add("カードを２枚引きます")
    layer.count = 0
    layer.moderate(PopStat(code=code))

def _handraw(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if layer.count >= 2:
        moderator.pop()
        return
    layer.count += 1
    moderator.append(handraw_layer(layer.delivery, layer.hoyuusya, code=code))

turn_draw_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="手札を２枚引く", delivery=delivery, gotoes={
        POP_OPEN: lambda l, s: _open(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _handraw(l, s, POP_ACT1)
    }, code=POP_TURN_DRAWED)
