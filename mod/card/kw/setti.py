#                 20                  40                  60                 79
from mod.const import enforce, side_name, OBAL_USE_CARD, IMG_NO_CHOICE,\
    CT_KOUGEKI, CT_DIV, TC_HUSEHUDA, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3,\
    POP_ACT4, POP_ACT5, POP_ACT6, POP_ACT7, SC_UROUO_SETTI
from mod.classes import PopStat, Card, Huda, Delivery, moderator
from mod.card.temp_koudou import auto_di
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.use_card_layer import use_card_layer
from mod.coous.scalar_correction import applied_scalar

_no_choice = Card(img=IMG_NO_CHOICE, name="何もしない", cond=auto_di, type=CT_DIV)

def _urouo_check(layer: PipelineLayer, stat: PopStat, urouo_code: int, not_code: int) -> None:
    if applied_scalar(i=0, scalar=SC_UROUO_SETTI, delivery=layer.delivery) > 0:
        layer.moderate(PopStat(urouo_code))
    else:
        layer.moderate(PopStat(not_code))

def _urouo_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    li: list[Huda] = []
    for huda in delivery.taba(hoyuusya, TC_HUSEHUDA):
        if isinstance(huda, Huda) and "setti" in huda.card.kwargs and\
        huda.card.can_play(delivery, hoyuusya) and huda.card.type != CT_KOUGEKI:
            li.append(huda)
    return li

def _choice_urouo(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    moderator.append(OnlySelectLayer(layer.delivery, layer.hoyuusya, "虚魚で追加起動する設置の選択",
        lower=_urouo_hudas(layer.delivery, layer.hoyuusya), upper=[_no_choice], code=code))

def _setti_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    li: list[Huda] = []
    for huda in delivery.taba(hoyuusya, TC_HUSEHUDA):
        if isinstance(huda, Huda) and "setti" in huda.card.kwargs and\
        huda.card.can_play(delivery, hoyuusya):
            li.append(huda)
    return li

def _choice_setti(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    moderator.append(OnlySelectLayer(layer.delivery, layer.hoyuusya, "起動する設置の選択",
        lower=_setti_hudas(layer.delivery, layer.hoyuusya), upper=[_no_choice], code=code))

def _use_setti(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    huda = enforce(stat.huda, Huda).base
    if huda.card.name == "何もしない":
        layer.moderate(PopStat(code))
        return
    layer.delivery.m_params(huda.hoyuusya).use_from_husehuda = True
    name = f"設置された{side_name(layer.hoyuusya)}の「{huda.card.name}」を使います"
    moderator.append(use_card_layer(cards=[huda.card], name=name, youso=huda,
                                    mode=OBAL_USE_CARD, code=code))

def _after_setti(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.m_params(layer.hoyuusya).use_from_husehuda = False
    layer.delivery.m_params(layer.hoyuusya).played_standard = False
    layer.moderate(PopStat(code))

def setti_layer(layer: PipelineLayer, stat: PopStat, code: int) -> PipelineLayer:
    return PipelineLayer("設置", layer.delivery, layer.hoyuusya, gotoes={
        POP_OPEN: lambda l, s: _urouo_check(l, s, POP_ACT1, POP_ACT4),
        POP_ACT1: lambda l, s: _choice_urouo(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: _use_setti(l, s, POP_ACT3),
        POP_ACT3: lambda l, s: _after_setti(l, s, POP_ACT4),
        POP_ACT4: lambda l, s: _choice_setti(l, s, POP_ACT5),
        POP_ACT5: lambda l, s: _use_setti(l, s, POP_ACT6),
        POP_ACT6: lambda l, s: _after_setti(l, s, POP_ACT7),
        POP_ACT7: lambda l, s: moderator.pop()
    }, code=code)
