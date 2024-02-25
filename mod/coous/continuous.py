#                 20                  40                  60                 79
from typing import TYPE_CHECKING, Optional, Callable, Protocol, runtime_checkable

if TYPE_CHECKING:
    from mod.card.card import Card, TaiounizeDI  # 循環import回避のために追加
    from mod.huda.huda import Huda
from mod.delivery import Delivery
BoolDII = Callable[[Delivery, int, int], bool]
auto_dii: BoolDII = lambda delivery, atk_h, cf_h: True

@runtime_checkable
class Continuous(Protocol):
    name: str
    type: int
    cond: BoolDII

# class Continuous():
# #                 20                  40                  60                 79
#     def __init__(self, name: str, type: int=0,
#     cond: BoolDII=auto_dih, taiounize: Optional['TaiounizeDI']=None,
#     trigger: int=0, card: Optional['Card']=None) -> None:
#         self.name = name
#         self.type = type
#         self.cond = cond
#         self.taiounize = taiounize
#         self.trigger = trigger
#         self.card = card

#     def __str__(self) -> str:
#         return f"Continuous{vars(self)}"
