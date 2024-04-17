from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        for i, card in enumerate(self.bmn.cards):
            screen.blit(source=card.zh.img, dest=[i*64, 0])