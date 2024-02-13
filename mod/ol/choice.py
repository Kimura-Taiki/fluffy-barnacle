#                 20                  40                  60                 79
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, TC_SUTEHUDA
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card
from mod.tf.taba_factory import TabaFactory
from mod.controller import controller
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.pop_stat import PopStat

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
SCALE_SIZE = 180

class Choice():
    def __init__(self, cards: list[Card], delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = "効果の選択"
        self.inject_func = delivery.inject_view
        factory = TabaFactory(inject_kwargs={
            "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": self._mousedown, "mouseup": self._mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        self.taba = factory.maid_by_cards(cards=cards, hoyuusya=self.hoyuusya)

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Any | None:
        return self.taba.get_hover_huda() or view_youso

    def open(self) -> None:
        ...

    def close(self) -> PopStat:
        return PopStat()

    def moderate(self, stat: PopStat) -> None:
        ...

    def _mousedown(self, huda: Huda) -> None:
        controller.active = huda

    def _mouseup(self, huda: Huda) -> None:
        # popup_message.add(text="PlayKougeki.mouseup でクリック確定したよ")
        huda.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya)
        if self.source_huda:
            self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
        moderator.pop()


# compatible_with(, OverLayer)
