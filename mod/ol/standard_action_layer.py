#                 20                  40                  60                 79
from mod.const import enforce, POP_OK, POP_OPEN, POP_VALIDATED_HUDA,\
    POP_VALIDATED_CARD, POP_CHOICED, POP_KAIKETUED, POP_PLAYED_STANDARD,\
    TC_HUSEHUDA, UC_SYUUTYUU, UC_ZYOGAI, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, TC_SUTEHUDA
from mod.classes import Callable, Any, PopStat, Card, Youso, Huda, Delivery, moderator,\
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

#                 20                  40                  60                 79
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
#                 20                  40                  60                 79

# def standard_layer(cards: list[Card], huda: Huda) ->PipelineLayer:
#     return PipelineLayer(name="StandardBasicActionLayer", delivery=huda.
#         delivery, hoyuusya=huda.hoyuusya, gotoes={
# POP_OPEN: lambda l, s: _validate_huda(l, s, POP_VALIDATED_HUDA),
# POP_VALIDATED_HUDA: lambda l, s: _validate_card(l, s, cards, POP_VALIDATED_CARD),
# POP_VALIDATED_CARD: lambda l, s: moderator.append(OnlySelectLayer(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, name="基本動作の選択", lower=list(s.rest_taba),
#     code=POP_CHOICED)),
# POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, code=POP_KAIKETUED),
# POP_KAIKETUED: lambda l, s: _play_standard(l, s, POP_PLAYED_STANDARD),
# POP_PLAYED_STANDARD: _tehuda_kihondousa
#         }, huda=huda)


# #                 20                  40                  60                 79
# def _validate_huda(layer: PipelineLayer, stat: PopStat, code: int) -> None:
#     if not enforce(layer.huda, Huda).can_standard(True):
#         moderator.pop()
#         return
#     layer.moderate(stat._replace(code=code))

# def _validate_card(layer: PipelineLayer, stat: PopStat,
# cards: list[Card], code: int) -> None:
#     li = [card for card in cards if card.can_play(layer.delivery, layer.
#         hoyuusya)]
#     if not li:
#         cards[0].can_play(layer.delivery, layer.hoyuusya, True)
#         moderator.pop()
#         return
#     layer.moderate(stat._replace(code=code, rest_taba=li))

# def _play_standard(layer: PipelineLayer, stat: PopStat, code: int) -> None:
#     layer.delivery.m_params(layer.hoyuusya).played_standard = True
#     layer.moderate(stat._replace(code=code))

# def _tehuda_kihondousa(layer: PipelineLayer, stat: PopStat) -> None:
#     layer.delivery.send_huda_to_ryouiki(huda=layer.huda, is_mine=True, taba_code=TC_HUSEHUDA)
#     moderator.pop()

# def _syuutyuu_kihondousa(layer: PipelineLayer, stat: PopStat) -> None:
#     layer.delivery.send_ouka_to_ryouiki(hoyuusya=layer.hoyuusya, from_mine=
#         True, from_code=UC_SYUUTYUU, to_code=UC_ZYOGAI)
#     moderator.pop()

# #                 20                  40                  60                 79
# def standard_tehuda_layer(cards: list[Card], huda: Huda) ->PipelineLayer:
#     return PipelineLayer(name="StandardBasicActionLayer", delivery=huda.
#         delivery, hoyuusya=huda.hoyuusya, gotoes={
# POP_OPEN: lambda l, s: _validate_huda(l, s, POP_VALIDATED_HUDA),
# POP_VALIDATED_HUDA: lambda l, s: _validate_card(l, s, cards, POP_VALIDATED_CARD),
# POP_VALIDATED_CARD: lambda l, s: moderator.append(OnlySelectLayer(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, name="基本動作の選択", lower=list(s.rest_taba),
#     code=POP_CHOICED)),
# POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, code=POP_KAIKETUED),
# POP_KAIKETUED: lambda l, s: _play_standard(l, s, POP_PLAYED_STANDARD),
# POP_PLAYED_STANDARD: _tehuda_kihondousa
#         }, huda=huda)

# def standard_syuutyuu_layer(cards: list[Card], huda: Youso) -> PipelineLayer:
#     return POP_PLAYED_STANDARD(name="StandardBasicActionLayer", delivery=huda.
#         delivery, hoyuusya=huda.hoyuusya, gotoes={
# POP_OPEN: lambda l, s: _validate_card(l, s, cards, POP_VALIDATED_CARD),
# POP_VALIDATED_CARD: lambda l, s: moderator.append(OnlySelectLayer(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, name="基本動作の選択", lower=list(s.rest_taba),
#     code=POP_CHOICED)),
# POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=huda.
#     delivery, hoyuusya=huda.hoyuusya, code=POP_KAIKETUED),
# POP_KAIKETUED: lambda l, s: _play_standard(l, s, POP_PLAYED_STANDARD),
# POP_PLAYED_STANDARD: _syuutyuu_kihondousa
#         }, huda=huda)



# def _others_basic_action_layer(
#         delivery: Delivery, hoyuusya: int, name: str="", huda: Any | None=None, cards:
#         list[Card]=[], mode: int=OBAL_KIHONDOUSA, code: int=POP_OK) -> MonoChoiceLayer:
#     # レイヤーの雛形を作る。
#     mcl = MonoChoiceLayer(
#         name=name if name else "<OthersBasicActionLayer>", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
#         mode=mode, moderate=_moderate, code=code)
#     # ファクトリーを準備する。
#     factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
#     # OBAL_定数に応じて、mc_layer.taba属性を修正する。
#     if mode == OBAL_KIHONDOUSA or mode == OBAL_SYUUTYUU:
#         mcl.taba = factory.maid_by_cards(cards=cards, delivery=delivery, hoyuusya=hoyuusya)
#     elif mode == OBAL_USE_CARD:
#         mcl.taba = factory.maid_by_hudas(hudas=[enforce(huda, Huda)], hoyuusya=hoyuusya)
#     # カード以外をクリックした際にメイン側へ戻れる様にmc_layer.other_hover属性を修正する。
#     mcl.other_hover = make_undo_youso(text="OthersBasicAction")
#     return mcl
