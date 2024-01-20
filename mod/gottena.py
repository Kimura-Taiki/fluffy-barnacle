from functools import partial
from typing import Callable, Any

from mod.gottenon import Gottenon
from mod.taba import Taba

class Gottena(list[Gottenon]):
    @staticmethod
    def _not_implemented_call(taba: Any=None) -> None:
        raise NotImplementedError("Gottena.call が未定義です")

    def __init__(self, data: list[Gottenon]=[], call: Callable[[Taba], None]=_not_implemented_call):
        super().__init__(data)
        self.selected = self[1]
        self.selected.on()
        self.call: Callable[[Taba], None] = call
        [gottenon.set_partial_attr(attr="hover", func=partial(self._hover_gottenon, gottena=self)) for gottenon in self]

    def elapse(self) -> None:
        [gottenon.draw() for gottenon in self]

    def get_hover_gotten(self) -> Gottenon | None:
        return next((gottenon for gottenon in self[::-1] if gottenon.is_cursor_on()), None)

    @staticmethod
    def _hover_gottenon(gottenon: Gottenon, gottena: 'Gottena') -> None:
        if gottena.selected == gottenon:
            return
        gottena.selected.off()
        gottenon.on()
        gottena.selected = gottenon
        gottena.call(taba=gottenon.taba)
