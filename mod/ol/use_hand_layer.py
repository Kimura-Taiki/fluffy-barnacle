#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, POP_CHOICED, POP_KAIKETUED,\
    TC_HUSEHUDA, UC_SYUUTYUU, UC_ZYOGAI, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, USAGE_DEPLOYED,\
    TC_MISIYOU, TC_YAMAHUDA, TC_SUTEHUDA, POP_CLOSED,\
    IMG_ZENRYOKUIZE
from mod.classes import Any, Callable, PopStat, Card, Youso, Huda, Taba, moderator,\
    popup_message
from mod.delivery import Delivery, duck_delivery
from mod.ol.pipeline_layer import PipelineLayer, _type_dummy
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.choice import choice_layer

_END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def _zenryokuize(layer: PipelineLayer, code: int) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, card = enforce(layer.huda, Huda), enforce(layer.card, Card)
    zenryokued = copy(enforce(card.kwargs["zenryokued"], Card))
    zenryokued.img = IMG_ZENRYOKUIZE
    moderator.append(choice_layer(cards=[card, zenryokued], delivery=delivery,
        hoyuusya=hoyuusya, huda=huda, code=code))

def _open(layer: PipelineLayer, stat: PopStat, text: str, code: int) -> None:
    print("open開始")
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, card = enforce(layer.huda, Huda), enforce(layer.card, Card)
    popup_message.add(text)
    if "zenryokuize" in card.kwargs and not delivery.m_params(hoyuusya).played_standard:
        print("全力化分岐")
        _zenryokuize(layer=layer, code=code)
    else:
        print("普通分岐")
        card.kaiketu(delivery, hoyuusya, huda=huda, code=code)
    print("open終了")

def _spend_huda(layer: PipelineLayer, huda: Huda) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, card = enforce(layer.huda, Huda), enforce(layer.card, Card)
    if delivery.b_params.sukinagasi:
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_YAMAHUDA, is_top=True)
        delivery.b_params.sukinagasi = False
    elif card.name == "麻痺毒" or card.name == "幻覚毒":
        ...
    else:
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_SUTEHUDA)

def _kaiketued_use_card(layer: PipelineLayer, huda: Huda, card: Card) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, card = enforce(layer.huda, Huda), enforce(layer.card, Card)
    if "ensin" in card.kwargs:
        delivery.m_params(hoyuusya).played_ensin = True
    if card.zenryoku and not delivery.m_params(hoyuusya).during_accelr:
        delivery.m_params(hoyuusya).played_zenryoku = True
    if card.syuutan:
        delivery.m_params(hoyuusya).played_syuutan = True
    if card.kirihuda:
        if huda.usage != USAGE_DEPLOYED:
            huda.usage = USAGE_USED
    else:
        _spend_huda(layer=layer, huda=huda)

def _kaiketued(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    print("kaiketued開始", layer.card, layer.huda)
    if stat.card:
        layer.card = stat.card
    print("statを確認", stat)
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, card = enforce(layer.huda, Huda), enforce(layer.card, Card)
    print("kaiketu", stat, stat.huda.card.name if stat.huda else None, stat.card.name if stat.card else None)
    delivery.m_params(layer.hoyuusya).played_standard = True
    _kaiketued_use_card(layer=layer, huda=huda, card=card)
    layer.moderate(PopStat(code))
    print("kaiketued終了")

def _closed(layer: PipelineLayer, stat: PopStat) -> None:
    if layer.mode == OBAL_USE_CARD:
        layer.delivery.m_params(layer.hoyuusya).use_card_count += 1

def use_hand_layer(name: str, card: Card, huda: Huda, code: int=POP_OK) -> PipelineLayer:
    from mod.const import side_name
    print("UHL開始", card, card.name, huda.card.name, side_name(huda.hoyuusya))
    delivery, hoyuusya = huda.delivery, huda.hoyuusya
    print("delivery, hoyuusyaを確定")
    if not card.can_play(delivery, hoyuusya, True):
        popup_message.add("Card.can_play == False分岐")
        return _END_LAYER(code)
    print("Card.can_play判定")
    if not huda.can_standard(True, True):
        popup_message.add("Huda.can_standard == False分岐")
        return _END_LAYER(code)
    print("Huda.can_standard判定")
    return PipelineLayer(name="手札からカードを使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, name, POP_ACT1),
POP_ACT1: lambda l, s: _kaiketued(l, s, POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop(),
POP_CLOSED: _closed
        }, huda=huda.base, card=card, code=code)



