from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen
from mod.view.tehuda_square import TehudaSquare
from ptc.element import Element

from pygame import Rect
from mod.card import Card

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn
        self.squares = [TehudaSquare(bmn.taba(hs=1, cr=CR_TEHUDA), Rect(340, 480, 600, 240)),
                        TehudaSquare(bmn.taba(hs=2, cr=CR_TEHUDA), Rect(340, 0, 600, 240), True)]

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        for square in self.squares:
            if element := square.get_hover():
                return element
        return None

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()
        # if hover := self.get_hover():
        #     screen.fill(color=(255, 0, 0), rect=((hover.dest)-(10, 10), (20, 20)))

from pygame import Rect
from mod.const.ryouiki import CR_YAMAHUDA, CR_TEHUDA, CR_KIRIHUDA
from mod.card import Card
from zh import z00_a as za
from zh import z00_b as zb

cards1 = [Card(zh=zh, hoyuusya=1, ryouiki={CR_TEHUDA}) for zh in [za.n_1, za.n_2, za.n_3]]
cards2 = [Card(zh=zh, hoyuusya=1, ryouiki={CR_YAMAHUDA}) for zh in [za.n_4, za.n_5, za.n_6, za.n_7]]
cards3 = [Card(zh=zh, hoyuusya=1, ryouiki={CR_KIRIHUDA}) for zh in [za.s_1, za.s_2, za.s_3]]
cards4 = [Card(zh=zh, hoyuusya=2, ryouiki={CR_TEHUDA}) for zh in [zb.n_1, zb.n_2, zb.n_3]]
cards5 = [Card(zh=zh, hoyuusya=2, ryouiki={CR_YAMAHUDA}) for zh in [zb.n_4, zb.n_5, zb.n_6, zb.n_7]]
cards6 = [Card(zh=zh, hoyuusya=2, ryouiki={CR_KIRIHUDA}) for zh in [zb.s_1, zb.s_2, zb.s_3]]

bmn = Banmen(cards=cards1+cards2+cards3+cards4+cards5+cards6)
view = BanmenView(bmn=bmn)
