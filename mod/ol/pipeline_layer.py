#                 20                  40                  60                 79
from mod.const import enforce, pass_func, POP_OK, POP_OPEN, POP_CLOSED
from mod.classes import Callable, Any, PopStat, Card, Huda, Youso, Delivery
from mod.ol.over_layer import OverLayer

def _type_dummy(pipe: 'PipelineLayer', stat: PopStat) -> None:
    raise EOFError("gotoesがデフォルト値のままです")

class PipelineLayer(OverLayer):
    def __init__(self, name: str, delivery: Delivery, hoyuusya: int=-1,
    gotoes: dict[int, Callable[['PipelineLayer', PopStat], None]]={POP_OK:
    _type_dummy}, card: Card | None=None, huda: Huda | None=None,
    rest: list[Any]=[], mode: int=0, code: int=POP_OK) -> None:
        self.name = name
        self.inject_func = pass_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player if hoyuusya == -1 else hoyuusya
        self.gotoes = gotoes
        self.card = card
        self.huda = huda
        self.rest = rest
        self.mode = mode
        self.code = code
        self.count = 0

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        self.moderate(PopStat(POP_OPEN))

    def close(self) -> PopStat:
        if closed := self.gotoes.get(POP_CLOSED):
            closed(self, PopStat())
        return PopStat(code=self.code, huda=self.huda, card=self.card, rest_taba=self.rest)

    def moderate(self, stat: PopStat) -> None:
        enforce(self.gotoes.get(stat.code), type(_type_dummy))(self, stat)
