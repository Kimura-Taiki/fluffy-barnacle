import pygame
from typing import Callable

from mod.const import compatible_with, WX, WY, pass_func, screen, IMG_GRAY_LAYER, BRIGHT, TC_HUSEHUDA
from mod.delivery import Delivery, duck_delivery
from mod.moderator import moderator
from mod.ol.over_layer import OverLayer
from mod.taba import Taba
from mod.youso import Youso
from mod.huda import Huda
from mod.controller import controller
from mod.kihondousa import zensin, ridatu, koutai, matoi, yadosi
from mod.ol.undo_mouse import make_undo_youso
from mod.ol.pop_stat import PopStat
from mod.ol.proxy_taba_factory import ProxyTabaFactory

_card_list = [pygame.image.load(f"pictures/{i}.png").convert_alpha() for i in [
    "kihon_zensin", "kihon_ridatu", "kihon_koutai", "kihon_matoi", "kihon_yadosi"]]

_undo_youso = make_undo_youso(text="OthersBasicAction")

class OthersBasicAction():
    def __init__(self, huda: Huda, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "基本動作の選択"
        self.source_huda = huda
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.hoyuusya = huda.hoyuusya
        self.taba: Taba

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.taba.elapse()

    def get_hover(self) -> Youso | None:
        return self.taba.get_hover_huda() or _undo_youso

    def open(self) -> None:
        bac = ProxyTabaFactory(inject_kwargs={"mouseup": self._mouseup})
        self.taba = bac.maid_by_files(surfaces=_card_list, hoyuusya=self.delivery.turn_player)
        for i, v in enumerate([zensin, ridatu, koutai, matoi, yadosi]):
            self.taba[i].koudou = v

    def close(self) -> PopStat:
        return PopStat()

    def moderate(self, stat: PopStat) -> None:
        ...

    def _mouseup(self, huda: Huda) -> None:
        huda.koudou(self.delivery, self.hoyuusya)
        self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_HUSEHUDA)
        moderator.pop()

compatible_with(OthersBasicAction(Huda(img=pygame.Surface((16, 16)))), OverLayer)