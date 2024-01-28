import pygame
from typing import Protocol, Callable, Any

from mod.const import compatible_with, WX, WY, SIMOTE, KAMITE, pass_func, screen, IMG_GRAY_LAYER
from mod.delivery import Delivery, duck_delivery
from mod.moderator import OverLayer
from mod.huda import default_draw
from mod.taba import Taba
from mod.taba_factory import TabaFactory
from mod.popup_message import popup_message
from mod.youso import Youso
from mod.huda import Huda

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0

_basic_action_factory = TabaFactory(inject_kwargs={"draw": default_draw, "hover": Huda.detail_draw}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
_card_list = [pygame.image.load(f"pictures/{i}.png").convert_alpha() for i in [
    "kihon_zensin", "kihon_ridatu", "kihon_koutai", "kihon_matoi", "kihon_yadosi"]]
_gray_youso = Youso()

class OthersBasicAction():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.taba: Taba

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Youso | None:
        return self.taba.get_hover_huda() or _gray_youso

    def open(self) -> None:
        popup_message.add(text="OthersBasicAction.openで開いたよ")
        self.taba = _basic_action_factory.maid_by_files(surfaces=_card_list, hoyuusya=self.delivery.turn_player)

    def close(self) -> int:
        popup_message.add(text="OthersBasicAction.openで閉じたよ")
        return 0

    def moderate(self, stat: int) -> None:
        ...

compatible_with(OthersBasicAction(), OverLayer)