#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable, Protocol, runtime_checkable, TypeVar, Any

from mod.const import enforce, TC_KIRIHUDA, USAGE_USED, USAGE_UNUSED, CT_KOUDOU
from mod.delivery import Delivery
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.coous.trigger import Trigger, BoolDII

BoolDI = Callable[[Delivery, int], bool]
KoukaDI = Callable[[Delivery, int], None]
auto_di: BoolDI = lambda delivery, hoyuusya: True

def saiki_kouka(card_name: str) -> KoukaDI:
    def func(delivery: Delivery, hoyuusya: int) -> None:
        if not (huda := next((huda for huda in enforce(
            delivery.taba_target(hoyuusya=hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA),
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
    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int) -> None:
        ...
#                 20                  40                  60                 79
def saiki_card(cls: type[_ProtCard], file_name: str, name: str) -> Any:
    return cls(img=pygame.image.load(file_name), name="再起："+name,
    cond=auto_di, type=CT_KOUDOU, kouka=saiki_kouka(card_name=name))

def saiki_trigger(cls: type[_ProtCard], file_name: str, name: str,
                  cond: BoolDII, trigger: int) -> Trigger:
    return Trigger(name=name, cond=cond, trigger=trigger, effect=saiki_card(
        cls=cls, file_name=file_name, name=name))

# _cfs_s_4 = Trigger(name="煌めきの乱舞", cond=auto_dii, trigger=TG_2_OR_MORE_DAMAGE, effect=_saiki_s_4)
