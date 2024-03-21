#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from mod.const import UC_MAAI, UC_AURA, UC_DUST, UC_FLAIR, UC_TATUZIN,\
    SC_TONZYUTU, SC_DEINEI
from mod.classes import Callable, Delivery, popup_message
from mod.card.card import BoolDI, Card, auto_di
from mod.coous.scalar_correction import applied_scalar

LOAD_SURFACE: Callable[[str], Surface] = lambda i: pygame.image.load(f"pictures/kihon_{i}.png").convert_alpha()

class KihonDousaCard(Card):
    def __init__(self, img: Surface, name: str, from_mine: bool, from_code: int,
                 to_mine: bool, to_code: int, add_cond: BoolDI=auto_di) -> None:
        cond: BoolDI = lambda delivery, hoyuusya: delivery.can_ouka_to_ryouiki(
            hoyuusya=hoyuusya, from_mine=from_mine, from_code=from_code,
            to_mine=to_mine, to_code=to_code) and add_cond(delivery, hoyuusya)
        super().__init__(img=img, name=name, cond=cond)
        def dousa(delivery: Delivery, hoyuusya: int) -> None:
            popup_message.add(f"{name}をします")
            delivery.send_ouka_to_ryouiki(
                hoyuusya=hoyuusya, from_mine=from_mine, from_code=from_code,
                to_mine=to_mine, to_code=to_code)
        self.kouka = dousa

#                 20                  40                  60                 79
zensin_booldi: BoolDI = lambda delivery, hoyuusya:\
    delivery.b_params.tatuzin_no_maai < delivery.b_params.maai and\
    applied_scalar(0, SC_TONZYUTU, delivery, hoyuusya) == 0
zensin_card: Card = KihonDousaCard(img=LOAD_SURFACE("zensin"), name="前進",
    from_mine=False, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA,
    add_cond=zensin_booldi)
ridatu_booldi: BoolDI = lambda delivery, hoyuusya:\
    delivery.b_params.tatuzin_no_maai >= delivery.b_params.maai and\
    applied_scalar(0, SC_DEINEI, delivery, hoyuusya) == 0
ridatu_card: Card = KihonDousaCard(img=LOAD_SURFACE("ridatu"), name="離脱",
    from_mine=False, from_code=UC_DUST, to_mine=False, to_code=UC_MAAI,
    add_cond=ridatu_booldi)
koutai_booldi: BoolDI = lambda delivery, hoyuusya:\
    applied_scalar(0, SC_DEINEI, delivery, hoyuusya) == 0
koutai_card: Card = KihonDousaCard(img=LOAD_SURFACE("koutai"), name="後退",
    from_mine=True, from_code=UC_AURA, to_mine=False, to_code=UC_MAAI,
    add_cond=koutai_booldi)
matoi_card: Card = KihonDousaCard(img=LOAD_SURFACE("matoi"), name="纏い", from_mine=False, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)
yadosi_card: Card = KihonDousaCard(img=LOAD_SURFACE("yadosi"), name="宿し", from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)
