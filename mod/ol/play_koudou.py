#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN
from mod.classes import Any, PopStat, Card, Huda, Delivery, moderator
from mod.ol.pipeline_layer import PipelineLayer

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    enforce(layer.card, Card).kouka(layer.delivery, layer.hoyuusya)
    if moderator.last_layer() == layer:
        moderator.pop()

def play_koudou_layer(card: Card, delivery: Delivery, hoyuusya: int,
                      huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    return PipelineLayer(name=f"行動:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: _open,
POP_OK: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)

class PlayKoudou():
    def __init__(self, card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int=POP_OK) -> None:
        self.card = card
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"行動:{card.name}の使用"
        self.inject_func = delivery.inject_view
        self.code = code

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        self.card.kouka(self.delivery, self.hoyuusya)
        if moderator.last_layer() == self:
            moderator.pop()

    def close(self) -> PopStat:
        self.card.close(hoyuusya=self.hoyuusya)
        return PopStat(self.code, self.source_huda)

    def moderate(self, stat: PopStat) -> None:
        moderator.pop()

# compatible_with(, OverLayer)
