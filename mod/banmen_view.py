from typing import runtime_checkable, Protocol

from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen

# @runtime_checkable
# class Element(Protocol):
#     def is_cursor_on(self) -> bool:
#         ...

#     def draw(self) -> None:
#         ...

# class Huda():
#     def __init__(self, card: Card) -> None:
#         pass

#     def is_cursor_on(self) -> bool:
#         return False

#     def draw(self) -> None:
#         ...

# HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
# HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

# HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
# HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

# HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
# HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

from pygame import Surface, Rect
from mod.card import Card
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class TehudaSquare():
    def __init__(self, cards: list[Card], rect: Rect) -> None:
        self.rect = rect
        self.img = Surface(rect.size)
        self.img.fill(color=RED)

    def draw(self) -> None:
        screen.blit(source=self.img, dest=self.rect.topleft)

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn
        self.squares = [TehudaSquare([], Rect(340, 480, 600, 240))]

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()
        # c1 = [card for card in self.bmn.cards if card.hoyuusya == 1 and CR_TEHUDA in card.ryouiki]
        # for i, card in enumerate(c1):
        #     screen.blit(source=card.zh.img, dest=[i*64, 0])
        # c2 = [card for card in self.bmn.cards if card.hoyuusya == 2 and CR_TEHUDA in card.ryouiki]
        # for i, card in enumerate(c2):
        #     screen.blit(source=card.zh.img, dest=[i*64, 320])

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
