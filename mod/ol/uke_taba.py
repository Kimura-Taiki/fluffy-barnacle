from typing import Callable
from functools import partial

from mod.const import WX, WY, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, side_name
from mod.delivery import Delivery
from mod.tf.taba_factory import TabaFactory
from mod.huda import Huda
from mod.taba import Taba
from mod.card import Kougeki, Damage
from mod.popup_message import popup_message

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0

def make_uke_taba(self, kougeki: Kougeki, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> Taba:
    mouseup = partial(_uke_mouseup, kougeki=kougeki, discard_source=discard_source, delivery=delivery, hoyuusya=hoyuusya)
    factory = _uke_factory(mouse_up=mouseup)
    _ad_card = Damage(img=IMG_AURA_DAMAGE, name="オーラで受けました", dmg=kougeki.aura_damage(
        delivery, hoyuusya), from_code=UC_AURA, to_code=UC_DUST)
    can_receive_aura = _ad_card.can_damage(delivery=delivery, hoyuusya=hoyuusya)
    _ld_card = Damage(img=IMG_LIFE_DAMAGE, name="ライフに通しました", dmg=kougeki.life_damage(
        delivery, hoyuusya), from_code=UC_LIFE, to_code=UC_FLAIR)
    return factory.maid_by_cards(cards=([_ad_card, _ld_card] if can_receive_aura else [_ld_card]), hoyuusya=hoyuusya)

def _uke_factory(mouse_up: Callable[[Huda], None]) -> TabaFactory:
    return TabaFactory(inject_kwargs={
        "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": mouse_up
        }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)

def _uke_mouseup(huda: Huda, kougeki: Kougeki, discard_source: Callable[[], None], delivery: Delivery, hoyuusya: int) -> None:
    huda.card.kaiketu(delivery=delivery, hoyuusya=hoyuusya)
    popup_message.add(f"{side_name(hoyuusya)}の「{kougeki.name}」を{huda.card.name}")
    discard_source()
