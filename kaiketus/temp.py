#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from typing import Callable, Protocol, runtime_checkable, TypeVar, Any

from mod.const import enforce, TC_KIRIHUDA, USAGE_USED, USAGE_UNUSED, CT_KOUDOU
from mod.delivery import Delivery
from mod.taba import Taba
from mod.popup_message import popup_message

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
#                 20                  40                  60                 79

# def saiki_card(file_name: str, name: str, kouka: Callable[[Delivery, int], None]) -> _ProtCard:
#     return _ProtCard(img=pygame.image.load(file_name), name="再起："+name,
#     cond=auto_di, type=CT_KOUDOU, kouka=saiki_kouka(card_name=name))
# T = TypeVar['T']
def saiki_card(cls: type[_ProtCard], file_name: str, name: str) -> Any:
    return cls(img=pygame.image.load(file_name), name="再起："+name,
    cond=auto_di, type=CT_KOUDOU, kouka=saiki_kouka(card_name=name))

# _saiki_s_4 = Card(img=pygame.image.load("cards/na_00_hajimari_b_s_4.png"), name="即再起：煌めきの乱舞", cond=auto_di, type=CT_KOUDOU,
#                   kouka=saiki_kouka(card_name="煌めきの乱舞"))
