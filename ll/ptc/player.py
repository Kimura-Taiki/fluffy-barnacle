from pygame import Color
from typing import runtime_checkable, Protocol

from mod.kard import Kard

@runtime_checkable
class Player(Protocol):
    name: str
    color: Color
    hand: Kard
    log: list[Kard]