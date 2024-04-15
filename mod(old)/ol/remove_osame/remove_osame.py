#                 20                  40                  60                 79
from mod.const import POP_OPEN, POP_SINGLE_ELAPSED
from mod.classes import PopStat, moderator, popup_message
from mod.ol.remove_osame.single_remove import single_remove_layer, huyo_hudas
from mod.ol.pipeline_layer import PipelineLayer
            
def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    popup_message.add("付与の納を償却します")
    layer.moderate(PopStat(code=code, rest_taba=huyo_hudas(delivery=
        layer.delivery, hoyuusya=layer.hoyuusya)))
    
def _single_elapsed(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    if not stat.rest_taba:
        moderator.pop()
    else:
        moderator.append(single_remove_layer(hudas=stat.rest_taba,
            delivery=layer.delivery, hoyuusya=layer.hoyuusya, code=code))

def remove_osame_layer(layer: PipelineLayer, code: int) -> PipelineLayer:
    return PipelineLayer(name="付与の償却", delivery=layer.delivery, hoyuusya=
        layer.hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_SINGLE_ELAPSED),
POP_SINGLE_ELAPSED: lambda l, s: _single_elapsed(l, s, POP_SINGLE_ELAPSED),
        }, code=code)