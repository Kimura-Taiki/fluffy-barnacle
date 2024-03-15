#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable, Protocol, runtime_checkable, TypeVar, Any

from mod.const import enforce, TC_KIRIHUDA, USAGE_USED, USAGE_UNUSED, CT_KOUDOU
from mod.delivery import Delivery
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.coous.trigger import Trigger, BoolDIIC

BoolDI = Callable[[Delivery, int], bool]
KoukaDI = Callable[[Delivery, int], None]
auto_di: BoolDI = lambda delivery, hoyuusya: True

def _saiki_kouka(card_name: str) -> KoukaDI:
    def func(delivery: Delivery, hoyuusya: int) -> None:
        if not (huda := next((huda for huda in enforce(
            delivery.taba(hoyuusya=hoyuusya, taba_code=TC_KIRIHUDA),
            Taba) if huda.card.name == card_name), None)):
            popup_message.add(f"切り札「{card_name}」が見つかりませんでした")
            return
        if huda.usage != USAGE_USED:
            return
        huda.usage = USAGE_UNUSED
        popup_message.add(f"切り札「{card_name}」が再起しました")
    return func

@runtime_checkable
class _ProtCard(Protocol):
    def __init__(self, img: Surface, name: str, cond: BoolDI, type: int,
                 kouka: Callable[[Delivery, int], None]) -> None:
        ...

def _saiki_card(cls: type[_ProtCard], file_name: str, name: str,
                img: Surface | None=None) -> Any:
    return cls(img=img if img else pygame.image.load(file_name), name="再起："+name,
    cond=auto_di, type=CT_KOUDOU, kouka=_saiki_kouka(card_name=name))

def saiki_trigger(cls: type[_ProtCard], name: str, cond: BoolDIIC,
trigger: int, file_name: str="", img: Surface | None=None) -> Trigger:
    return Trigger(name=name, cond=cond, trigger=trigger, effect=_saiki_card(
        cls=cls, file_name=file_name, name=name, img=img))
