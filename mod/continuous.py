#                 20                  40                  60                 79
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from mod.card import TaiounizeDI  # 循環import回避のために追加

from mod.const import CF_ATTACK_CORRECTION

class Continuous():
    def __init__(self, type: int=0, taiounize: Optional['TaiounizeDI']=None) -> None:
        self.type = type
        self.taiounize = taiounize