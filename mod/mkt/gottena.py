from functools import partial

from mod.mkt.gottenon import Gottenon

class Gottena(list[Gottenon]):
    def __init__(self, data: list[Gottenon]=[]):
        super().__init__(data)
        self.selected = self[1]
        self.selected.on()
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
