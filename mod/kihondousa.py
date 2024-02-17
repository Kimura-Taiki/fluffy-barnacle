#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Any, Callable
from mod.const import CT_HUTEI, UC_MAAI, UC_AURA, UC_DUST, UC_FLAIR
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.card import BoolDI, Card, KoukaDI, MaaiDI, SuuziDI, TaiounizeDI, auto_di, identity_di, int_di, pass_di, whole_di

LOAD_SURFACE: Callable[[str], Surface] = lambda i: pygame.image.load(f"pictures/kihon_{i}.png").convert_alpha()

class KihonDousaCard(Card):
    def __init__(self, img: Surface, name: str, from_mine: bool, from_code: int,
                 to_mine: bool, to_code: int) -> None:
        cond: BoolDI = lambda delivery, hoyuusya: delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=from_mine, from_code=from_code,
            to_mine=to_mine, to_code=to_code)
        super().__init__(img=img, name=name, cond=cond)
        def dousa(delivery: Delivery, hoyuusya: int) -> None:
            popup_message.add(f"{name}をします")
            delivery.send_ouka_to_ryouiki(
                hoyuusya=hoyuusya, from_mine=from_mine, from_code=from_code,
                to_mine=to_mine, to_code=to_code)
        self.kouka = dousa

zensin_card = KihonDousaCard(img=LOAD_SURFACE("zensin"), name="前進", from_mine=False, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)
ridatu_card = KihonDousaCard(img=LOAD_SURFACE("ridatu"), name="離脱", from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI)
koutai_card = KihonDousaCard(img=LOAD_SURFACE("koutai"), name="後退", from_mine=True, from_code=UC_AURA, to_mine=False, to_code=UC_MAAI)
matoi_card = KihonDousaCard(img=LOAD_SURFACE("matoi"), name="纏い", from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)
yadosi_card = KihonDousaCard(img=LOAD_SURFACE("yadosi"), name="宿し", from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)

def pass_koudou(delivery: Delivery, hoyuusya: int) -> None:
    pass

def can_zensin(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)

def zensin(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="前進します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)

def can_ridatu(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_MAAI)

def ridatu(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="離脱します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_MAAI)

def can_koutai(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_MAAI)

def koutai(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="後退します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_MAAI)

def can_matoi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)

def matoi(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="纏います")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)

def can_yadosi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)

def yadosi(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="宿します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)
