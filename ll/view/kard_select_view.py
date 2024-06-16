from pygame import Surface, Vector2 as V2, Rect, SRCALPHA
from math import sin, cos, radians

from any.func import ratio_rect, img_zoom, rect_fill, translucented_color
from any.screen import screen, WV2
# from seed.default_deck import _kards, KARD_BANPEI
from model.board import Board
from model.kard import Kard, EMPTY_KARD
from model.ui_element import UIElement
from ptc.bridge import Bridge
from view.kard_square import KardSquare
from view.progress_helper import ProgressHelper

_RATIO = V2(1280, 640)

from ptc.transition import Transition
class KardSelectView():
    def __init__(
            self, bridge: Bridge, rect: Rect=Rect((0, 0), WV2),
            canvas: Surface=screen
        ) -> None:
        _, self.in_progress, self._pre_complete, _, _, _\
            = ProgressHelper(seconds=0.0).provide_progress_funcs()
        self.rect = ratio_rect(rect=rect, ratio=_RATIO)
        self.canvas = canvas
        self.view = bridge.view
        self.set_kards = board_rest_kards(board=bridge.board)
        self.img = self._img()
        self.squares = self._squares()
        self._selected = False
        self.selected_kard: Kard = EMPTY_KARD

    def get_hover(self) -> UIElement | None:
        for square in self.squares[::-1]:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        self.view.draw()
        rect_fill(
            color=translucented_color(color="black", a=64),
            rect=Rect((0, 0), WV2),
            surface=self.canvas
        )
        self.canvas.blit(
            source=self.img,
            dest=self.rect.topleft
        )
        for square in self.squares:
            square.draw()

    def elapse(self) -> None:
        for square in self.squares:
            square.elapse()

    def _img(self) -> Surface:
        img = Surface(size=_RATIO, flags=SRCALPHA)
        return img_zoom(img=img,rect=self.rect, ratio=_RATIO)

    def _squares(self) -> list[KardSquare]:
        n = len(self.set_kards)
        return [self._kq(i=i, n=n) for i in range(n)]

    def _kq(self, i: int, n: int) -> KardSquare:
        r = 2303
        o_v2 = V2(640, r+375)
        deg = -10.0+20.0*i/(n-1)-90.0
        rad = radians(deg)
        i_v2 = o_v2+ie_v2_from_radian(radian=rad)*r
        kard = self.set_kards[i]
        ui_element = UIElement(
            mousedown=lambda : self._complete(kard=kard)
        )
        return KardSquare(
            kard=kard,
            angle=-(deg+90),
            scale=self.rect.w/_RATIO.x,
            center=i_v2,
            canvas=self.canvas,
            ui_element=ui_element
        )

    def _complete(self, kard: Kard) -> None:
        self.selected_kard = kard
        self._pre_complete()

def board_rest_kards(board: Board) -> list[Kard]:
    all_kards: list[Kard] = []
    all_kards.extend(board.reserve)
    all_kards.extend(board.deck)
    for player in board.players:
        all_kards.extend(player.hands)
    li: list[Kard] = []
    for kard in all_kards:
        if kard not in li:
            li.append(kard)
    return sorted(list(li), key=lambda kard: kard.rank)

def ie_v2_from_radian(radian: float) -> V2:
    return V2(cos(radian), sin(radian))
