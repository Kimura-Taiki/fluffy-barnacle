#                 20                  40                  60                 79
from mod.const import enforce, TC_YAMAHUDA, TC_TEHUDA, UC_AURA, UC_DUST,\
    UC_LIFE, UC_FLAIR, DMG_SYOUSOU, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE
from mod.classes import Huda, Delivery, moderator
from mod.card.damage import Damage
from mod.ol.only_select_layer import OnlySelectLayer

def _draw(delivery: Delivery, hoyuusya: int) -> None:
    draw_huda = enforce(delivery.taba_target(hoyuusya=hoyuusya,
                     is_mine=True, taba_code=TC_YAMAHUDA), list[Huda])[0]
    
    delivery.send_huda_to_ryouiki(huda=draw_huda, is_mine=True,
                                  taba_code=TC_TEHUDA)

def _adc() -> Damage:
    return Damage(img=IMG_AURA_DAMAGE, name="オーラ", dmg=1, from_code=UC_AURA,
                  to_code=UC_DUST, attr=DMG_SYOUSOU)

def _ldc() -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="ライフ", dmg=1, from_code=UC_LIFE,
                  to_code=UC_FLAIR, attr=DMG_SYOUSOU)

def _syousou(delivery: Delivery, hoyuusya: int) -> None:
    cards = [_adc(), _ldc()] if delivery.ouka_count(hoyuusya=
        hoyuusya, is_mine=True, utuwa_code=UC_AURA) > 0 else [_ldc()]
    moderator.append(OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya,
        name="焦燥ダメージ", upper=cards))

def is_yamahuda(delivery: Delivery, hoyuusya: int) -> bool:
    return len(enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True,
        taba_code=TC_YAMAHUDA), list)) > 0

def _handraw(delivery: Delivery, hoyuusya: int) -> None:
    (_draw if is_yamahuda(delivery, hoyuusya) else _syousou)(delivery, hoyuusya)