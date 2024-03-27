#                 20                  40                  60                 79
from pygame import Surface, SRCALPHA, Vector2

from mod.const import IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, IMG_BURST_DAMAGE,\
    UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, opponent, POP_OPEN, POP_ACT1,\
    POP_ACT2, draw_aiharasuu, FONT_SIZE_DAMAGE, CT_DIV, enforce
from mod.classes import Card, Delivery, moderator
from mod.card.card import auto_di
from mod.card.damage import Damage
from mod.coous.attack_correction import applied_kougeki
from mod.coous.aura_guard import huyo_aura_guard
from mod.ol.pipeline_layer import PipelineLayer

_0DAMAGE = Damage(img=IMG_AURA_DAMAGE, name="打ち消しました", dmg=0,
                  from_code=UC_AURA, to_code=UC_DUST)

def uke_cards(card: Card, delivery: Delivery, hoyuusya: int) -> list[Card]:
    applied = applied_kougeki(card, delivery, hoyuusya)
    aura_damage = applied.aura_damage(delivery, hoyuusya)
    life_damage = applied.life_damage(delivery, hoyuusya)
    if "burst" in card.kwargs:
        return [_burst_card(base_card=card, ad=aura_damage, ld=life_damage)]
    if aura_damage is None:
        return [_0DAMAGE] if life_damage is None else\
            [_ld_card(dmg=life_damage)]
    else:
        ad_card = _ad_card(dmg=aura_damage)
        if life_damage is None:
            return [ad_card]
        else:
            ld_card = _ld_card(dmg=life_damage)
            return [ad_card, ld_card] if _is_receivable(aura_damage=aura_damage,
                delivery=delivery, hoyuusya=opponent(hoyuusya)) else [ld_card]

def _img_burst(ad: int | None, ld: int | None) -> Surface:
    img = IMG_BURST_DAMAGE.copy()
    draw_aiharasuu(surface=img, dest=Vector2(340, 475)/2-Vector2(
        FONT_SIZE_DAMAGE, FONT_SIZE_DAMAGE)/2-(100, 100), num=enforce(ad, int),
        size=FONT_SIZE_DAMAGE)
    draw_aiharasuu(surface=img, dest=Vector2(340, 475)/2-Vector2(
        FONT_SIZE_DAMAGE, FONT_SIZE_DAMAGE)/2+(100, 100), num=enforce(ld, int),
        size=FONT_SIZE_DAMAGE)
    return img

def _burst_card(base_card: Card, ad: int | None, ld: int | None) -> Card:
    ad_card = _ad_card(dmg=ad) if ad else _ad_card(dmg=0)
    ld_card = _ld_card(dmg=ld) if ld else _ld_card(dmg=0)
    def kouka(delivery: Delivery, hoyuusya: int) -> None:
        moderator.append(PipelineLayer(name="両受けダメージの順次処理", delivery=delivery,
            hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: ad_card.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT1),
POP_ACT1: lambda l, s: ld_card.kaiketu(delivery=delivery, hoyuusya=hoyuusya, code=POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop()
            }))
    return Card(img=_img_burst(ad, ld), name="両受けダメージ", cond=auto_di,
                type=CT_DIV, megami=base_card.megami, kouka=kouka)

def _ad_card(dmg: int) -> Damage:
    return Damage(img=IMG_AURA_DAMAGE, name="オーラで防ぎました", dmg=dmg,
                  from_code=UC_AURA, to_code=UC_DUST)

def _ld_card(dmg: int) -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="ライフで受けました", dmg=dmg,
                  from_code=UC_LIFE, to_code=UC_FLAIR)

def _is_receivable(aura_damage: int, delivery: Delivery, hoyuusya: int) -> bool:
    huyo_aura = huyo_aura_guard(delivery=delivery, hoyuusya=hoyuusya)
    self_aura = delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_AURA)
    return huyo_aura+self_aura >= aura_damage
