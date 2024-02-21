#                 20                  40                  60                 79
from typing import Callable, Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, HANTE, POP_VIEWED_BANMEN, POP_OK, POP_EMPTY_TABA, enforce
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.taba import Taba
from mod.moderator import moderator
from mod.card import Card

class MonoChoiceLayer():
    def __init__(self, name: str="", taba: Taba=Taba(), delivery: Delivery=
                 duck_delivery, hoyuusya: int=HANTE, huda: Any | None=None,
                 card: Card | None=None,
                 moderate: Callable[['MonoChoiceLayer', PopStat], None]=
                 lambda mcl, stat: None, code: int=POP_OK) -> None:
        self.name = name
        self.taba = taba
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.card = card
        self.inject_func = delivery.inject_view
        self.other_hover = view_youso
        self.moderate_func = moderate
        self.code = code

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Any | None:
        return self.taba.get_hover_huda() or self.other_hover

    def open(self) -> None:
        if not self.taba:
            moderator.pop()
        elif len(self.taba) == 1:
            self.taba[0].mouseup()

    def close(self) -> PopStat:
        if not self.taba:
            return PopStat(code=POP_EMPTY_TABA)
        return PopStat(code=self.code, huda=self.source_huda, rest_taba=self.taba)

    def moderate(self, stat: PopStat) -> None:
        if stat.code == POP_VIEWED_BANMEN:
            return
        self.moderate_func(self, stat)

# compatible_with(, OverLayer)
        

