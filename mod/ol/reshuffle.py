#                 20                  40                  60                 79
from random import shuffle

from mod.const import TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA, USAGE_DEPLOYED,\
    IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU, enforce, opponent, IMG_LIFE_DAMAGE,\
    UC_LIFE, UC_FLAIR, DMG_RESHUFFLE, POP_RESHUFFLE_SELECTED
from mod.classes import Callable, Card, Huda, Taba, Delivery
from mod.card.card import auto_di
from mod.card.damage import Damage
from mod.ol.only_select_layer import OnlySelectLayer

def _reshuffle_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    taba1 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_YAMAHUDA), Taba)
    taba2 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_HUSEHUDA), Taba)
    taba3 = enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_SUTEHUDA), Taba)
    moto = list(taba1)+list(taba2)+[huda for huda in taba3 if huda.usage != USAGE_DEPLOYED]
    shuffle(moto)
    return moto

_damage = Damage(img=IMG_LIFE_DAMAGE, name="再構成ダメージです", dmg=1, from_code=
                 UC_LIFE, to_code=UC_FLAIR, attr=DMG_RESHUFFLE)

def _reshuffle_kouka(delivery: Delivery, hoyuusya: int) -> None:
    for huda in _reshuffle_hudas(delivery=delivery, hoyuusya=hoyuusya):
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=
                                      TC_YAMAHUDA)
    _damage.kaiketu(delivery=delivery, hoyuusya=opponent(hoyuusya))

_reshuffle_card = Card(img=IMG_BOOL_ZE, name="再構成", cond=auto_di, type=
                       CT_KOUDOU, kouka=_reshuffle_kouka)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_cards = [_reshuffle_card, _pass_card]

reshuffle_layer: Callable[[Delivery, int], OnlySelectLayer] = lambda delivery,\
    hoyuusya: OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya, name=\
    "再構成の選択", upper=_cards, code=POP_RESHUFFLE_SELECTED)
