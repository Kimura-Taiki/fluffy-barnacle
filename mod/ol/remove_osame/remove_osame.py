#                 20                  40                  60                 79
from mod.const import pass_func, enforce, POP_OK, POP_OPEN, POP_SINGLE_ELAPSED\
    , POP_HUYO_ELAPSED
from mod.classes import Callable, Any, PopStat, Huda, Delivery, moderator, popup_message
from mod.ol.remove_osame.single_remove import single_remove_layer, huyo_hudas
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        popup_message.add("付与の納を償却します")
        _append(delivery=self.delivery, hoyuusya=self.hoyuusya, hudas=
            huyo_hudas(delivery=self.delivery, hoyuusya=self.hoyuusya))

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        print("moderate", stat)
        if not stat.rest_taba:
            moderator.pop()
        else:
            _append(delivery=self.delivery, hoyuusya=self.hoyuusya,
                    hudas=stat.rest_taba)
            
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

def _append(delivery: Delivery, hoyuusya: int, hudas: list[Huda]) -> None:
    moderator.append(single_remove_layer(hudas=hudas, delivery=delivery,
        hoyuusya=hoyuusya, code=POP_OK))

                # 20                  40                  60                 79
def remove_osame_layer(layer: PipelineLayer) -> PipelineLayer:
    return PipelineLayer(name="付与の償却", delivery=layer.delivery, hoyuusya=
        layer.hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_SINGLE_ELAPSED),
POP_SINGLE_ELAPSED: lambda l, s: _single_elapsed(l, s, POP_SINGLE_ELAPSED),
        }, code=POP_HUYO_ELAPSED)