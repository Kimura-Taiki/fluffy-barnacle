from pygame import Color
from dataclasses import dataclass, field
from enum import Enum, auto

from any.func import ColorValue, lcgs
from model.kard import Kard

class Genus(Enum):
    OBS = auto()
    MAN = auto()
    COM = auto()

@dataclass
class Player():
    genus: Genus
    name: str
    color: Color
    hands: list[Kard] = field(default_factory=list)
    log: list[Kard] = field(default_factory=list)
    alive: bool=True
    protected: bool=False

    @property
    def hand(self) -> Kard:
        return self.hands[0]

    @property
    def view_hash(self) -> int:
        hash = (2 if self.alive else 3) * (5 if self.protected else 7)
        for kard in self.hands:
            hash = lcgs(hash, kard.view_hash, 11)
        for kard in self.log:
            hash = lcgs(hash, kard.view_hash, 13)
        return hash

    @classmethod
    def new_man(cls, name: str, color: ColorValue) -> 'Player':
        return Player(
            genus=Genus.MAN,
            name=name,
            color=Color(color),
            alive=True
        )


OBSERVER = Player(
    genus=Genus.OBS,
    name="(Observer)",
    color=Color("white")
)
