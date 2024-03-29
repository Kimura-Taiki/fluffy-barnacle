#                 20                  40                  60                 79
from copy import copy

from mod.const import enforce, POP_OK, POP_OPEN, POP_CHOICED, POP_KAIKETUED,\
    TC_HUSEHUDA, UC_SYUUTYUU, UC_ZYOGAI, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, USAGE_DEPLOYED,\
    TC_MISIYOU, TC_YAMAHUDA, TC_SUTEHUDA, POP_CLOSED,\
    IMG_ZENRYOKUIZE
from mod.classes import Callable, PopStat, Card, Youso, Huda, Taba, moderator,\
    popup_message
from mod.delivery import duck_delivery
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.choice import choice_layer

_END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def _zenryokuize(layer: PipelineLayer, huda: Huda, code: int) -> None:
    zenryokued = copy(enforce(huda.card.kwargs["zenryokued"], Card))
    zenryokued.img = IMG_ZENRYOKUIZE
    moderator.append(choice_layer(cards=[huda.card, zenryokued], delivery=layer.delivery,
        hoyuusya=layer.hoyuusya, huda=huda, code=code))

def _choiced(layer: PipelineLayer, stat: PopStat, text: str, code: int) -> None:
    popup_message.add(text)
    huda = enforce(stat.huda, Huda).base
    if "zenryokuize" in huda.card.kwargs and not layer.delivery.m_params(layer.hoyuusya).played_standard:
        _zenryokuize(layer=layer, huda=huda, code=code)
    else:
        huda.card.kaiketu(delivery=layer.delivery, hoyuusya=
            layer.hoyuusya, huda=layer.huda, code=code)

def _spend_huda(layer: PipelineLayer, huda: Huda) -> None:
    if layer.delivery.b_params.sukinagasi:
        layer.delivery.send_huda_to_ryouiki(huda=huda.base, is_mine=True, taba_code=TC_YAMAHUDA, is_top=True)
        layer.delivery.b_params.sukinagasi = False
    elif "tanki_doku" in enforce(layer.card, Card).kwargs:
        ...
    else:
        layer.delivery.send_huda_to_ryouiki(huda=huda.base, is_mine=True, taba_code=TC_SUTEHUDA)

def _kaiketued_use_card(layer: PipelineLayer, huda: Huda, card: Card) -> None:
    layer.card = card
    if "ensin" in card.kwargs:
        layer.delivery.m_params(layer.hoyuusya).played_ensin = True
    if card.zenryoku:
        layer.delivery.m_params(layer.hoyuusya).played_zenryoku = True
    if card.syuutan:
        layer.delivery.m_params(layer.hoyuusya).played_syuutan = True
    if huda.card.kirihuda:
        if huda.usage != USAGE_DEPLOYED:
            huda.base.usage = USAGE_USED
    else:
        _spend_huda(layer=layer, huda=huda)

def _kaiketued(layer: PipelineLayer, stat: PopStat) -> None:
    print("kaiketu", stat, stat.huda.card.name if stat.huda else None, stat.card.name if stat.card else None)
    layer.delivery.m_params(layer.hoyuusya).played_standard = True
    if layer.mode == OBAL_KIHONDOUSA:
        huda = enforce(layer.huda, Huda)
        layer.delivery.send_huda_to_ryouiki(huda=huda.base, is_mine=True,
            taba_code=TC_HUSEHUDA)
    elif layer.mode == OBAL_USE_CARD:
        _kaiketued_use_card(layer=layer, huda=enforce(layer.huda, Huda), card=enforce(stat.card, Card))
    elif layer.mode == OBAL_SYUUTYUU:
        layer.delivery.send_ouka_to_ryouiki(
            hoyuusya=layer.hoyuusya, from_mine=True, from_code=UC_SYUUTYUU,
            to_mine=False, to_code=UC_ZYOGAI)
    moderator.pop()

def _closed(layer: PipelineLayer, stat: PopStat) -> None:
    if layer.mode == OBAL_USE_CARD:
        layer.delivery.m_params(layer.hoyuusya).use_card_count += 1

def use_card_layer(cards: list[Card], name: str, youso: Youso, mode: int=
OBAL_KIHONDOUSA, code: int=POP_OK) -> PipelineLayer:
    delivery, hoyuusya = youso.delivery, youso.hoyuusya
    li = [card for card in cards if card.can_play(delivery, hoyuusya)]
    if not li:
        if cards:
            cards[0].can_play(delivery, hoyuusya, True)
        else:
            popup_message.add("集中力はカードではありません")
        return _END_LAYER(code)
    if isinstance(youso, Huda) and not youso.can_standard(True, True if mode == OBAL_USE_CARD else False):
        return _END_LAYER(code)
    return PipelineLayer(name="通常の方法によるカードの使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=delivery,
    hoyuusya=hoyuusya, name="基本動作の選択", lower=li, code=POP_CHOICED)),
POP_CHOICED: lambda l, s: _choiced(l, s, name, POP_KAIKETUED),
POP_KAIKETUED: _kaiketued,
POP_CLOSED: _closed
        },huda=youso if isinstance(youso, Huda) else None, mode=mode, code=code)
