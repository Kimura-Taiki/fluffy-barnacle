from pygame import Rect

from mod.screen import screen
from ptc.square import Square
from ptc.player import Player
from ptc.element import Element

class PlayerSquare():
    def __init__(self, player: Player, rect: Rect) -> None:
        self.player = player
        self.rect = rect

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        screen.fill(color=self.player.color, rect=self.rect)