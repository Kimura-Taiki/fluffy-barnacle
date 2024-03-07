#                 20                  40                  60                 79
from typing import Callable, Protocol, runtime_checkable

from mod.delivery import Delivery
BoolDII = Callable[[Delivery, int, int], bool]
'''BoolDIIは 盤面(Delivery), 呼び出した者(int), 永続札の保有者(int) の３引数構成'''
auto_dii: BoolDII = lambda delivery, atk_h, cf_h: True
mine_cf: BoolDII = lambda delivery, atk_h, cf_h: atk_h == cf_h

# @runtime_checkable
# class Continuous(Protocol):
class Continuous():
    name: str
    type: int
    cond: BoolDII
