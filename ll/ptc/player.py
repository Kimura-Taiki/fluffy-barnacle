from pygame import Color

from typing import runtime_checkable, Protocol

@runtime_checkable
class Player(Protocol):
    name: str
    color: Color