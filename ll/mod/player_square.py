from pygame import Rect, Color
from copy import deepcopy

from mod.screen import screen
from mod.func import rect_fill
from mod.font import MS_MINCHO_COL
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
        rect_fill(color=self.translucent_color, rect=self.rect)
        # screen.fill(color=self.translucent_color, rect=self.rect)
        screen.blit(source=MS_MINCHO_COL(self.player.name, 24, "black"), dest=self.rect)

    @property
    def translucent_color(self) -> Color:
        color = deepcopy(self.player.color)
        color.a = int(color.a/2)
        return color