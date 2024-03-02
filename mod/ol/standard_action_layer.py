#                 20                  40                  60                 79
from mod.const import enforce, POP_OPEN, POP_VALIDATED, POP_CHOICED,\
    POP_KAIKETUED
from mod.classes import PopStat, Card, Huda, Delivery, moderator,\
    popup_message
from mod.ol.turns_progression.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

#                 20                  40                  60                 79
def standard_basic_action_layer(cards: list[Card], huda: Huda, delivery:
Delivery, hoyuusya: int) ->PipelineLayer:
    return PipelineLayer(name="StandardBasicActionLayer", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
        POP_OPEN: lambda l, s: l.moderate(PopStat(POP_VALIDATED)),
        POP_VALIDATED: lambda l, s: moderator.append(OnlySelectLayer(delivery=
            delivery, hoyuusya=hoyuusya, name="基本動作の選択", lower=cards,
            code=POP_CHOICED)),
        POP_CHOICED: lambda l, s: enforce(s.huda, Huda).card.kaiketu(delivery=
            delivery, hoyuusya=hoyuusya, code=POP_KAIKETUED),
        POP_KAIKETUED: lambda l, s: moderator.pop()
    }, huda=huda)

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
