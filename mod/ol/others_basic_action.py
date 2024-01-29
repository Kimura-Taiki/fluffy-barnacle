import pygame
from typing import Protocol, Callable, Any
from functools import partial

from mod.const import compatible_with, WX, WY, SIMOTE, KAMITE, pass_func, screen, IMG_GRAY_LAYER, BRIGHT, TC_HUSEHUDA
from mod.delivery import Delivery, duck_delivery
from mod.moderator import OverLayer, moderator
from mod.huda import default_draw
from mod.taba import Taba
from mod.taba_factory import TabaFactory
from mod.popup_message import popup_message
from mod.youso import Youso
from mod.huda import Huda
from mod.controller import controller

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0

def _mousedown(huda: Huda) -> None:
    popup_message.add(text="OthersBasicAction.mousedown でクリックしたよ")
    controller.active = huda

def _mouseup(huda: Huda) -> None:
    moderator.pop()

_basic_action_factory = TabaFactory(inject_kwargs={
    "draw": default_draw, "hover": Huda.detail_draw
    }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
_card_list = [pygame.image.load(f"pictures/{i}.png").convert_alpha() for i in [
    "kihon_zensin", "kihon_ridatu", "kihon_koutai", "kihon_matoi", "kihon_yadosi"]]
_gray_youso = Youso(mousedown=_mousedown, mouseup=_mouseup)

class OthersBasicAction():
    def __init__(self, huda: Huda, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.source_huda = huda
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.taba: Taba

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Youso | None:
        return self.taba.get_hover_huda() or _gray_youso

    def open(self) -> None:
        popup_message.add(text="OthersBasicAction.open で開いたよ")
        bac = TabaFactory(inject_kwargs={
            "draw": self._draw, "hover": Huda.detail_draw, "mousedown": self._mousedown, "mouseup": self._mouseup
            }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
        self.taba = bac.maid_by_files(surfaces=_card_list, hoyuusya=self.delivery.turn_player)
        print(self.taba[0].hoyuusya)

    def close(self) -> int:
        popup_message.add(text="OthersBasicAction.close で閉じたよ")
        return 0

    def moderate(self, stat: int) -> None:
        ...

    def _draw(self, huda: Huda) -> None:
        if controller.hover == huda:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
            screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
        else:
            default_draw(huda=huda)

    def _mousedown(self, huda: Huda) -> None:
        popup_message.add(text="OthersBasicAction.mousedown でクリックしたよ")
        controller.active = huda

    def _mouseup(self, huda: Huda) -> None:
        huda.koudou(self.delivery, self.delivery.turn_player)
        print(huda.hoyuusya, self.delivery.turn_player)
        self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
        moderator.pop()



compatible_with(OthersBasicAction(Huda(img=pygame.Surface((16, 16)))), OverLayer)