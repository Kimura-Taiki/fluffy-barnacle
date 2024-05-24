from pygame import Color
from typing import NamedTuple
from enum import Enum, auto

from any.func import ColorValue
from model.kard import Kard, EMPTY_KARD

class Genus(Enum):
    OBS = auto()
    MAN = auto()
    COM = auto()

class Player(NamedTuple):
    genus: Genus
    name: str
    color: Color
    hand: Kard=EMPTY_KARD
    log: list[Kard]=[]
    alive: bool=True

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

players: list[Player] = []
for PLAYER in players:
    ...