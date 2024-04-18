from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        c1 = [card for card in self.bmn.cards if card.hoyuusya == 1]
        for i, card in enumerate(c1):
            screen.blit(source=card.zh.img, dest=[i*64, 0])
        c2 = [card for card in self.bmn.cards if card.hoyuusya == 2]
        for i, card in enumerate(c2):
            screen.blit(source=card.zh.img, dest=[i*64, 320])

from mod.card import Card
from zh import z00_a as za
from zh import z00_b as zb

cards1 = [Card(zh=zh, hoyuusya=1, ryouiki={0}) for zh in [za.n_1, za.n_2, za.n_3, za.n_4, za.n_5, za.n_6, za.n_7]]
cards2 = [Card(zh=zh, hoyuusya=2, ryouiki={0}) for zh in [zb.n_1, zb.n_2, zb.n_3, zb.n_4, zb.n_5, zb.n_6, zb.n_7]]

bmn = Banmen(cards=cards1+cards2)
view = BanmenView(bmn=bmn)
