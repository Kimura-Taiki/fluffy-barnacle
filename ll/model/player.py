from pygame import Color
from dataclasses import dataclass, field
from enum import Enum, auto

from any.func import ColorValue
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
