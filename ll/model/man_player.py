from pygame import Color

from any.func import ColorValue
from model.kard import Kard, EMPTY_KARD

from ptc.player import Player
class ManPlayer():
    def __init__(self, name: str, color: ColorValue, log: list[Kard]) -> None:
        self.name = name
        self.color = Color(color)
        self.hand = EMPTY_KARD
        self.log = log
        self.alive = True