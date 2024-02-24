#                 20                  40                  60                 79
from typing import Any

from mod.const import TC_HUSEHUDA, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, UC_DUST, UC_AURA, UC_FLAIR, UC_LIFE
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda.huda import Huda
from mod.ol.undo_mouse import make_undo_youso
from mod.tf.taba_factory import TabaFactory
from mod.card.card import Card, Damage
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat

def _uke_cards(card: Card, delivery: Delivery, hoyuusya: int) -> list[Card]:
    ad_card = Damage(img=IMG_AURA_DAMAGE, name="オーラで受けました", dmg=card.aura_damage(
        delivery, hoyuusya), from_code=UC_AURA, to_code=UC_DUST)
    ld_card = Damage(img=IMG_LIFE_DAMAGE, name="ライフに通しました", dmg=card.life_damage(
        delivery, hoyuusya), from_code=UC_LIFE, to_code=UC_FLAIR)
    can_receive_aura = ad_card.can_damage(delivery=delivery, hoyuusya=hoyuusya)
    return [ad_card, ld_card] if can_receive_aura and not card.aura_bar(delivery, hoyuusya) else [ld_card]

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def play_kougeki_layer(card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None=None) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name=f"攻撃:{card.name}の使用", delivery=delivery, hoyuusya=hoyuusya, huda=huda,
                          moderate=_moderate, card=card)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=_uke_cards(card=card, delivery=delivery, hoyuusya=hoyuusya), hoyuusya=hoyuusya)
    mcl.other_hover = make_undo_youso(text="OthersBasicAction")
    return mcl
