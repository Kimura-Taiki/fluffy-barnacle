#                 20                  40                  60                 79
from mod.const import side_name, opponent, enforce, POP_OK, POP_OPEN,\
    POP_CHOICED, POP_TAIOUED, POP_KAIKETUED, POP_AFTER_ATTACKED, OBAL_USE_CARD
from mod.classes import Any, PopStat, Card, Huda, Delivery, moderator,\
    popup_message
from mod.ol.play_kougeki.uke_cards import uke_cards
from mod.ol.play_kougeki.taiou_hudas import taiou_hudas
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.card.damage import Damage
from mod.ol.use_card_layer import use_card_layer
from mod.coous.attack_correction import AttackCorrection

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    card = enforce(layer.card, Card)
    if not card.can_play(delivery=delivery, hoyuusya=hoyuusya, popup=True):
        moderator.pop()
        return
    layer.delivery.b_params.attack_megami = card.megami
    upper = uke_cards(card=card, delivery=delivery, hoyuusya=hoyuusya)
    lower = taiou_hudas(card=card, delivery=delivery, hoyuusya=hoyuusya)
    if stat.switch or layer.delivery.b_params.during_taiou:
        lower.clear()
    moderator.append(OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya,
        name=f"{side_name(opponent(hoyuusya))}の「{card.name}」受け選択",
        lower=lower, upper=upper, code=code))


#                 20                  40                  60                 79
def _cfs(layer: PipelineLayer, cf_h: int) -> list[AttackCorrection]:
    gggg = [cf for cf in layer.delivery.m_params(hoyuusya=cf_h).lingerings
        if isinstance(cf, AttackCorrection) and cf.cond(layer.delivery,
        layer.hoyuusya, cf_h, enforce(layer.card, Card))]
    
def _choiced(layer: PipelineLayer, stat: PopStat, uke_code: int,
             taiou_code: int) -> None:
    huda, kougeki = enforce(stat.huda, Huda), enforce(layer.card, Card)
    if isinstance(huda.card, Damage):
        popup_message.add(f"{side_name(layer.hoyuusya)}の「{kougeki.name}」を"\
                          f"{huda.card.name}")
        huda.card.kaiketu(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                          code=uke_code)
        return
    layer.delivery.b_params.during_taiou = True
    moderator.append(use_card_layer(cards=[huda.card], name=
        f"{side_name(huda.hoyuusya)}は対応して「{huda.card.name}」を使います",
        youso=huda, mode=OBAL_USE_CARD, code=taiou_code))

def _taioued(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.b_params.during_taiou = False
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, kougeki = enforce(stat.huda, Huda), enforce(layer.card, Card)
    if not kougeki.maai_cond(delivery=delivery, hoyuusya=hoyuusya):
        popup_message.add(text=f"{side_name(hoyuusya)}の「{kougeki.name}」が"\
                          "適正距離から外れました")
        moderator.pop()
        return
    layer.card = huda.card.taiounize(kougeki, delivery, hoyuusya)
    layer.moderate(stat=PopStat(code=code, switch=True))

def _kaiketued(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    kougeki = enforce(layer.card, Card)
    if kougeki.after:
        kougeki.after.kaiketu(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                              huda=layer.huda, code=code)
        return
    moderator.pop()

def play_kougeki_layer(card: Card, delivery: Delivery, hoyuusya: int,
                       huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    layer = PipelineLayer(name=f"攻撃:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_CHOICED),
POP_CHOICED: lambda l, s: _choiced(l, s, POP_KAIKETUED, POP_TAIOUED),
POP_TAIOUED: lambda l, s: _taioued(l, s, POP_OPEN),
POP_KAIKETUED: lambda l, s: _kaiketued(l, s, POP_AFTER_ATTACKED),
POP_AFTER_ATTACKED: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)
    return layer
