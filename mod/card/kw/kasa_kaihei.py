#                 20                  40                  60                 79
from mod.const import enforce, IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU,\
    POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Card, Huda, Delivery, moderator
from mod.card.card import auto_di
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer

def _kaihei_kouka(delivery: Delivery, hoyuusya: int) -> None:
    delivery.m_params(hoyuusya).henbou = not delivery.m_params(hoyuusya).henbou

_kaihei_card = Card(img=IMG_BOOL_ZE, name="傘の開閉", cond=auto_di, type=
                       CT_KOUDOU, kouka=_kaihei_kouka)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_cards = [_kaihei_card, _pass_card]

def kasa_kaihei_layer(delivery: Delivery, hoyuusya: int, code: int) -> PipelineLayer:
    return PipelineLayer("傘の開閉", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya,
            name=f"傘の開閉　現在{"開(ホロビ)" if delivery.m_params(hoyuusya).henbou else "閉(ユキノ)"}",
            upper=_cards, code=code)),
        POP_ACT1: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }, code=code)

# kasa_kaihei_layer: Callable[[Delivery, int], OnlySelectLayer] = lambda delivery,\
#     hoyuusya: OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya, name=\
#     f"傘の開閉　現在{"開(ホロビ)" if delivery.m_params(hoyuusya).henbou else "閉(ユキノ)"}",
#     upper=_cards, code=POP_RESHUFFLE_SELECTED)
