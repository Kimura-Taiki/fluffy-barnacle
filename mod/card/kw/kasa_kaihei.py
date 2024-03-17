#                 20                  40                  60                 79
from mod.const import enforce, IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU,\
    POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TC_TEHUDA, UC_AURA
from mod.classes import PopStat, Card, Huda, Delivery, moderator
from mod.card.card import auto_di
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.yazirusi import Yazirusi

def _has_kasamawasi(delivery: Delivery, hoyuusya: int) -> bool:
    li: list[Huda] = delivery.taba(hoyuusya, TC_TEHUDA)
    return any(huda.card.name == "かさまわし" for huda in li)

_kasamawasi_card = Card(img=IMG_BOOL_ZE, name="かさまわし", cond=auto_di, type=CT_KOUDOU,
    kouka=Yazirusi(to_mine=True, to_code=UC_AURA).send)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_kasamawasi_cards = [_kasamawasi_card, _pass_card]

def _kaihei_kouka(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).henbou = not delivery.m_params(hoyuusya).henbou
    if _has_kasamawasi(delivery, hoyuusya):
        moderator.append(PipelineLayer("かさまわし", delivery, hoyuusya, gotoes={
            POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya,
                name="かさまわしでのオーラ回収の選択",
                upper=_kasamawasi_cards, code=POP_ACT1)),
            POP_ACT1: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT2),
            POP_ACT2: lambda l, s: moderator.pop()
        }))

_kaihei_card = Card(img=IMG_BOOL_ZE, name="傘の開閉", cond=auto_di, type=
                       CT_KOUDOU, kouka=_kaihei_kouka)
_kaihei_cards = [_kaihei_card, _pass_card]

def kasa_kaihei_layer(delivery: Delivery, hoyuusya: int, code: int) -> PipelineLayer:
    return PipelineLayer("傘の開閉", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: l.moderate(PopStat(POP_ACT1 if delivery.m_params(hoyuusya).has_yukihi else POP_ACT3)),
        POP_ACT1: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya,
            name=f"傘の開閉　現在{"開(ホロビ)" if delivery.m_params(hoyuusya).henbou else "閉(ユキノ)"}",
            upper=_kaihei_cards, code=POP_ACT2)),
        POP_ACT2: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }, code=code)
