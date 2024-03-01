#                 20                  40                  60                 79
from mod.const import enforce, pass_func, POP_OPEN
from mod.classes import Callable, PopStat, Youso, Delivery
from mod.ol.over_layer import OverLayer

class PipelineLayer(OverLayer):
    def __init__(self, name: str, delivery: Delivery, gotoes: dict[int,
    Callable[['PipelineLayer', PopStat], None]], code: int) -> None:
        self.name = name
        self.inject_func = pass_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player
        self.gotoes = gotoes
        self.code = code
        self.count = 0

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        self.moderate(PopStat(code=POP_OPEN))

    def close(self) -> PopStat:
        return PopStat(code=self.code)

    def moderate(self, stat: PopStat) -> None:
        enforce(self.gotoes.get(stat.code), type(_type_dummy))(self, stat)

def _type_dummy(pipe: PipelineLayer, stat: PopStat) -> None:
    ...
