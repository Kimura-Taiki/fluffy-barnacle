#                 20                  40                  60                 79
from mod.const import enforce, IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU,\
    POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, TC_TEHUDA, UC_AURA, TG_KAIHEI
from mod.classes import PopStat, Card, Huda, Delivery, moderator
from mod.card.card import auto_di
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.yazirusi import Yazirusi
from mod.coous.trigger import solve_trigger_effect

_kasamawasi_card = Card(img=IMG_BOOL_ZE, name="かさまわし", cond=auto_di, type=CT_KOUDOU,
    kouka=Yazirusi(to_mine=True, to_code=UC_AURA).send)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_kasamawasi_cards = [_kasamawasi_card, _pass_card]

def _practical_kaihei(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.m_params(layer.hoyuusya).henbou = not layer.delivery.m_params(layer.hoyuusya).henbou
    layer.moderate(PopStat(code))

def _has_kasamawasi(delivery: Delivery, hoyuusya: int) -> bool:
    li: list[Huda] = delivery.taba(hoyuusya, TC_TEHUDA)
    return any(huda.card.name == "かさまわし" for huda in li)

def _kasamawasi(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    if _has_kasamawasi(delivery, hoyuusya):
        moderator.append(PipelineLayer("かさまわし", delivery, hoyuusya, gotoes={
            POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya,
                name="かさまわしでのオーラ回収の選択",
                upper=_kasamawasi_cards, code=POP_ACT1)),
            POP_ACT1: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT2),
            POP_ACT2: lambda l, s: moderator.pop()
        }, code=code))
    else:
        layer.moderate(PopStat(code))

def _trigger(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    solve_trigger_effect(delivery=layer.delivery, hoyuusya=layer.hoyuusya, trigger=TG_KAIHEI, code=code)

def _kaihei_kouka(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("傘の開閉の実処理", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _practical_kaihei(l, s, POP_ACT1),
        POP_ACT1: lambda l, s: _kasamawasi(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _trigger(l, s, POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }))

kaihei_card = Card(img=IMG_BOOL_ZE, name="傘の開閉", cond=auto_di, type=
                       CT_KOUDOU, kouka=_kaihei_kouka)
_kaihei_cards = [kaihei_card, _pass_card]

def kasa_kaihei_layer(delivery: Delivery, hoyuusya: int, code: int) -> PipelineLayer:
    return PipelineLayer("傘の開閉の選択", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: l.moderate(PopStat(POP_ACT1 if delivery.m_params(hoyuusya).has_yukihi else POP_ACT3)),
        POP_ACT1: lambda l, s: moderator.append(OnlySelectLayer(delivery, hoyuusya,
            name=f"傘の開閉　現在{"開(ホロビ)" if delivery.m_params(hoyuusya).henbou else "閉(ユキノ)"}",
            upper=_kaihei_cards, code=POP_ACT2)),
        POP_ACT2: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery, hoyuusya, code=POP_ACT3),
        POP_ACT3: lambda l, s: moderator.pop()
    }, code=code)
