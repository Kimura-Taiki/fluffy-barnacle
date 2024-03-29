#                 20                  40                  60                 79
from typing import Any
import pygame
from pygame.surface import Surface
from mod.const import enforce, UC_MAAI, UC_AURA, UC_DUST, UC_FLAIR, UC_TATUZIN,\
    SC_TONZYUTU, SC_DEINEI, CT_DIV,\
    POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5
from mod.classes import Callable, PopStat, Delivery, moderator, popup_message
from mod.card.card import BoolDI, Card, auto_di
from mod.card.kw.yazirusi import Yazirusi, ya_zensin, ya_ridatu, ya_koutai,\
    ya_matoi, ya_yadosi
from mod.coous.scalar_correction import applied_scalar
from mod.ol.pipeline_layer import PipelineLayer

LOAD_SURFACE: Callable[[str], Surface] = lambda i: pygame.image.load(f"pictures/kihon_{i}.png").convert_alpha()

def _pmes(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    popup_message.add(f"{layer.name}をします")
    layer.moderate(PopStat(code))

class KihonDousa(Card):
    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None = None, code: int = POP_OK) -> None:
        moderator.append(PipelineLayer(f"基本動作「{self.name}」", delivery, hoyuusya, gotoes={
            POP_OPEN: lambda l, s: _pmes(l, s, POP_ACT1),
            POP_ACT1: lambda l, s: super(KihonDousa, self).kaiketu(delivery, hoyuusya, huda, POP_ACT2),
            POP_ACT2: lambda l, s: moderator.pop()
        }, card=self, code=code))

zensin_booldi: BoolDI = lambda delivery, hoyuusya:\
    ya_zensin.can_send(delivery, hoyuusya) and\
    delivery.b_params.tatuzin_no_maai < delivery.b_params.maai and\
    applied_scalar(0, SC_TONZYUTU, delivery, hoyuusya) == 0
zensin_card = KihonDousa(img=LOAD_SURFACE("zensin"), name="前進",
    cond=zensin_booldi, type=CT_DIV, kouka=ya_zensin.send)

ridatu_booldi: BoolDI = lambda delivery, hoyuusya:\
    ya_ridatu.can_send(delivery, hoyuusya) and\
    delivery.b_params.tatuzin_no_maai >= delivery.b_params.maai and\
    applied_scalar(0, SC_DEINEI, delivery, hoyuusya) == 0
ridatu_card = KihonDousa(img=LOAD_SURFACE("ridatu"), name="離脱",
    cond=ridatu_booldi, type=CT_DIV, kouka=ya_ridatu.send)

koutai_booldi: BoolDI = lambda delivery, hoyuusya:\
    ya_koutai.can_send(delivery, hoyuusya) and\
    applied_scalar(0, SC_DEINEI, delivery, hoyuusya) == 0
koutai_card = KihonDousa(img=LOAD_SURFACE("koutai"), name="後退",
    cond=koutai_booldi, type=CT_DIV, kouka=ya_koutai.send)

matoi_card = KihonDousa(img=LOAD_SURFACE("matoi"), name="纏い",
    cond=ya_matoi.can_send, type=CT_DIV, kouka=ya_matoi.send)

yadosi_card = KihonDousa(img=LOAD_SURFACE("yadosi"), name="宿し",
    cond=ya_yadosi.can_send, type=CT_DIV, kouka=ya_yadosi.send)

kd_list = [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card]