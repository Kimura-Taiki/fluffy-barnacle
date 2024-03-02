#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_CHOICED, POP_KAIKETUED,\
    TC_HUSEHUDA, UC_SYUUTYUU, UC_ZYOGAI, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, TC_SUTEHUDA
from mod.classes import Callable, PopStat, Card, Youso, Huda, moderator,\
    popup_message
from mod.delivery import duck_delivery
from mod.ol.turns_progression.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

_END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def _play_standard(layer: PipelineLayer, stat: PopStat) -> None:
    layer.delivery.m_params(layer.hoyuusya).played_standard = True
    if layer.mode == OBAL_KIHONDOUSA:
        layer.delivery.send_huda_to_ryouiki(huda=layer.huda, is_mine=True,
            taba_code=TC_HUSEHUDA)
    elif layer.mode == OBAL_USE_CARD:
        huda = enforce(layer.huda, Huda)
        if huda.card.zenryoku:
            layer.delivery.m_params(layer.hoyuusya).played_zenryoku = True
        if huda.card.kirihuda:
            huda.usage = USAGE_USED
        else:
            layer.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True,
                                                taba_code=TC_SUTEHUDA)
    elif layer.mode == OBAL_SYUUTYUU:
        layer.delivery.send_ouka_to_ryouiki(
            hoyuusya=layer.hoyuusya, from_mine=True, from_code=UC_SYUUTYUU,
            to_mine=False, to_code=UC_ZYOGAI)
    moderator.pop()

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
    if isinstance(youso, Huda) and not youso.can_standard(True):
        return _END_LAYER(code)
    return PipelineLayer(name="通常の方法によるカードの使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: moderator.append(OnlySelectLayer(delivery=delivery,
    hoyuusya=hoyuusya, name="基本動作の選択", lower=li, code=POP_CHOICED)),
POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=delivery,
    hoyuusya=youso.hoyuusya, huda=youso, code=POP_KAIKETUED),
POP_KAIKETUED: _play_standard,
        },huda=youso if isinstance(youso, Huda) else None, mode=mode, code=code)
