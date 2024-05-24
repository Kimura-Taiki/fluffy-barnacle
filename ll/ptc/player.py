from pygame import Color
from typing import runtime_checkable, Protocol, NamedTuple

from model.kard import Kard, EMPTY_KARD

@runtime_checkable
class Player(Protocol):
    name: str
    color: Color
    hand: Kard
    log: list[Kard]
    alive: bool

class _ObserverPlayer():
    def __init__(self) -> None:
        self.name = "(Observer)"
        self.color = Color("white")
        self.hand = EMPTY_KARD
        self.log: list[Kard] = []
        self.alive = False

OBSERVER = _ObserverPlayer()