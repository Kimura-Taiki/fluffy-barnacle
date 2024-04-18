from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        for i, card in enumerate(self.bmn.cards):
            screen.blit(source=card.zh.img, dest=[i*64, 0])

from mod.card import Card
from zh.z00_a import n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9

bmn = Banmen(cards=[Card(zh=zh) for zh in [n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9]])
view = BanmenView(bmn=bmn)
