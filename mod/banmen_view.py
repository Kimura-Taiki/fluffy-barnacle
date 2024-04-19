from typing import runtime_checkable, Protocol

from mod.const.screen import screen, IMG_YATUBA_BG
from mod.banmen import Banmen

from pygame import Surface, Rect, Vector2 as V2, transform
from typing import Callable
from math import sin, cos, radians
from mod.card import Card
RED = (255, 0, 0)
BLUE = (0, 0, 255)

@runtime_checkable
class Element(Protocol):
    def is_cursor_on(self) -> bool:
        ...

    def draw(self) -> None:
        ...

class Huda():
    def __init__(self, img: Surface, mid: V2, angle: float, scale: float) -> None:
        hx, hy = V2(img.get_size())/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        self.vertices = [self._rotated_vertices(ov=mid, iv=vec, angle=angle) for vec in li]
        self.img = transform.rotozoom(surface=img, angle=angle, scale=scale)
        self.dest = mid-V2(self.img.get_size())/2

    def is_cursor_on(self) -> bool:
        return False

    def draw(self) -> None:
        screen.blit(source=self.img, dest=self.dest)

    def _rotated_vertices(self, ov: V2, iv: V2, angle: float) -> V2:
        rad = radians(-angle)
        return V2(ov.x+(cos(rad)*iv.x-sin(rad)*iv.y),
                  ov.y+(sin(rad)*iv.x+cos(rad)*iv.y))

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[Rect, int, int], float] = lambda r, i, j: r.centerx-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[Rect, int, int], float] = lambda r, i, j: r.bottom-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

class TehudaSquare():
    def __init__(self, cards: list[Card], rect: Rect, is_reverse: bool = False) -> None:
        self.cards = cards
        self.rect = rect
        j = len(cards)
        self.hudas = [Huda(
            img=card.zh.img,
            mid=V2(rect.centerx*2-HAND_X(rect, i, j), rect.centery*2-HAND_Y(rect, i, j))
                if is_reverse else V2(HAND_X(rect, i, j), HAND_Y(rect, i, j)),
            angle=HAND_ANGLE(i, j)+(180.0 if is_reverse else 0.0),
            scale=0.6)
            for i, card in enumerate(cards)]

    def draw(self) -> None:
        for huda in self.hudas:
            huda.draw()

class BanmenView():
    def __init__(self, bmn: Banmen) -> None:
        self.bmn = bmn
        self.squares = [TehudaSquare(bmn.taba(hs=1, cr=CR_TEHUDA), Rect(340, 480, 600, 240)),
                        TehudaSquare(bmn.taba(hs=2, cr=CR_TEHUDA), Rect(340, 0, 600, 240), True)]

    def rearrange(self) -> None:
        ...

    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        for square in self.squares:
            square.draw()

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
