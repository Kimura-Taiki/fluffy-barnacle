#                 20                  40                  60                 79
from typing import Callable, Protocol, runtime_checkable

from mod.delivery import Delivery

@runtime_checkable
class _Card(Protocol):
    megami: int

BoolDIIC = Callable[[Delivery, int, int, _Card], bool]
'''BoolDIIは 盤面(Delivery), 呼び出した者(int), 永続札の保有者(int) の３引数構成'''
auto_diic: BoolDIIC = lambda delivery, atk_h, cf_h, card: True
mine_cf: BoolDIIC = lambda delivery, atk_h, cf_h, card: atk_h == cf_h

# @runtime_checkable
# class Continuous(Protocol):
class Continuous():
    name: str
    type: int
    cond: BoolDIIC
