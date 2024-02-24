#                 20                  40                  60                 79
from typing import TYPE_CHECKING, Optional, Callable

if TYPE_CHECKING:
    from mod.card import TaiounizeDI  # 循環import回避のために追加
    from mod.huda.huda import Huda
from mod.delivery import Delivery
BoolDII = Callable[[Delivery, int, int], bool]
auto_dih: BoolDII = lambda delivery, atk_h, cf_h: True

from mod.const import CF_ATTACK_CORRECTION

class Continuous():
    def __init__(self, name: str, type: int=0, cond: BoolDII=auto_dih, taiounize: Optional['TaiounizeDI']=None) -> None:
        self.name = name
        self.type = type
        self.cond = cond
        self.taiounize = taiounize

    def __str__(self) -> str:
        return f"Continuous{vars(self)}"
