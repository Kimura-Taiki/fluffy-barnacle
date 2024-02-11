#                 20                  40                  60                 79
from pygame.math import Vector2
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, TC_SUTEHUDA, side_name
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery

SCALE_SIZE = 180

class PlayHuyo():
    def __init__(self, card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.card = card
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"付与:{card.name}の使用"
        self.inject_func = delivery.inject_view

    def elapse(self) -> None:
        screen.blit(source=self.card.img, dest=-Vector2(self.card.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])

    def get_hover(self) -> Any | None:
        return view_youso

    def open(self) -> None:
        ...

    def close(self) -> int:
        popup_message.add("解決した！？")
        self.card.close(hoyuusya=self.hoyuusya)
        return 0

    def moderate(self, stat: Any) -> None:
        ...

# compatible_with(, OverLayer)
