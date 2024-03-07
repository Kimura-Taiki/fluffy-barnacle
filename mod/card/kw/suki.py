#                 20                  40                  60                 79
import pygame
from pygame import Surface

from mod.const import enforce, DMG_RESHUFFLE, TC_SUTEHUDA, UC_DUST, CT_HUYO,\
    USAGE_DEPLOYED, USAGE_USED, TG_1_OR_MORE_DAMAGE
from mod.classes import Any, Card, Taba, Delivery, popup_message
from mod.coous.continuous import BoolDIIC
from mod.coous.trigger import Trigger
from mod.card.card import auto_di, BoolDI, SuuziDI
from mod.card.temp_koudou import TempKoudou

# _cond_n_9: BoolDIIC = lambda delivery, call_h, cf_h, card: delivery.b_params.damage_attr != DMG_RESHUFFLE

# def _kouka_n_9(delivery: Delivery, hoyuusya: int) -> None:
#     if not (huda := next((huda for huda in enforce(delivery.taba_target(
#     hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba) if
#     huda.card.name == "陰の罠"), None)):
#         popup_message.add(f"付与札「陰の罠」が見つかりませんでした")
#         return
#     if huda.usage != USAGE_DEPLOYED:
#         return
#     delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_huda=huda, to_code=UC_DUST, kazu=99)
#     huda.usage = USAGE_USED
#     popup_message.add("隙を突かれたので「陰の罠」を破棄します")

# _effect_n_9 = TempKoudou(name="陰の罠：隙", cond=auto_di, kouka=_kouka_n_9)

# _cfs_n_9 = Trigger(name="陰の罠", cond=_cond_n_9, trigger=TG_1_OR_MORE_DAMAGE, effect=_effect_n_9)

# n_9 = Card(megami=MG_UTURO, img=pygame.image.load("cards/na_00_hajimari_a_n_9.png"), name="陰の罠", cond=auto_di, type=CT_HUYO,
#            osame=int_di(2), suki=auto_di, hakizi=_atk_n_9, cfs=[_cfs_n_9])

#                 20                  40                  60                 79
def _kouka(delivery: Delivery, hoyuusya: int, name: str) -> None:
    if not (huda := next((huda for huda in enforce(delivery.taba_target(
    hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba) if
    huda.card.name == name), None)):
        popup_message.add(f"付与札「{name}」が見つかりませんでした")
        return
    if huda.usage != USAGE_DEPLOYED:
        return
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_huda=huda,
                                  to_code=UC_DUST, kazu=99)
    huda.usage = USAGE_USED
    popup_message.add(f"隙を突かれたので「{name}」を破棄します")

def _effect(name: str) -> Card:
    return TempKoudou(name=f"{name}：隙", cond=auto_di, kouka=lambda d, h:
                      _kouka(delivery=d, hoyuusya=h, name=name))

_not_reshuffle: BoolDIIC = lambda delivery, call_h, cf_h, card:\
    delivery.b_params.damage_attr != DMG_RESHUFFLE

def _cfs(name: str) -> Trigger:
    return Trigger(name=name, cond=_not_reshuffle, trigger=TG_1_OR_MORE_DAMAGE,
                   effect=_effect(name=name))

def suki_card(megami: int, img: Surface, name: str, cond: BoolDI,
              osame: SuuziDI, hakizi: Card, **kwargs: Any) -> Card:
    return Card(megami=megami, img=img, name=name, cond=cond, type=CT_HUYO,
        osame=osame, suki=auto_di, hakizi=hakizi, cfs=[_cfs(name=name)], **kwargs)
