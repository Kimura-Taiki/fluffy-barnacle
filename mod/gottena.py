from mod.gottenon import Gottenon

class Gottena(list[Gottenon]):
    def __init__(self, data: list[Gottenon]=[]):
        super().__init__(data)
        self.selected = self[1]
        self.selected.on()

    def elapse(self) -> None:
        [gottenon.draw() for gottenon in self]