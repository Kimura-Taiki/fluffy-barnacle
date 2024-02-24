#                 20                  40                  60                 79
from random import shuffle

from mod.const import TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA, USAGE_DEPLOYED,\
    IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU, enforce, POP_RESHUFFLED, IMG_LIFE_DAMAGE, UC_LIFE, UC_FLAIR, opponent
from mod.delivery import Delivery
from mod.moderator import moderator
from mod.huda.huda import Huda
from mod.tf.taba_factory import TabaFactory
from mod.card import Card, auto_di, Damage
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat
from mod.taba import Taba

def _reshuffle_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    taba1 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_YAMAHUDA), Taba)
    taba2 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_HUSEHUDA), Taba)
    taba3 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba)
    moto = list(taba1)+list(taba2)+[huda for huda in taba3 if huda.usage != USAGE_DEPLOYED]
    shuffle(moto)
    return moto

damage = Damage(img=IMG_LIFE_DAMAGE, name="再構成ダメージです", dmg=1, from_code=UC_LIFE, to_code=UC_FLAIR)

def _reshuffle_kouka(delivery: Delivery, hoyuusya: int) -> None:
    for huda in _reshuffle_hudas(delivery=delivery, hoyuusya=hoyuusya):
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_YAMAHUDA)
    damage.kaiketu(delivery=delivery, hoyuusya=opponent(hoyuusya))

_reshuffle_card = Card(img=IMG_BOOL_ZE, name="再構成", cond=auto_di, type=CT_KOUDOU, kouka=_reshuffle_kouka)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_cards = [_reshuffle_card, _pass_card]

def _mouseup(huda: Huda) -> None:
    huda.card.kaiketu(huda.delivery, huda.hoyuusya)

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def reshuffle_layer(delivery: Delivery, hoyuusya: int) -> MonoChoiceLayer:
    mcl = MonoChoiceLayer(name="再構成の選択", delivery=delivery, hoyuusya=hoyuusya, moderate=_moderate, code=POP_RESHUFFLED)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=_cards, hoyuusya=hoyuusya)
    return mcl
