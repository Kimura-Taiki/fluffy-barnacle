from pygame.surface import Surface
from typing import NamedTuple

from mod.const import TC_INVALID, compatible_with
from mod.huda import Huda
from mod.request import Request

_duck_huda = Huda(img=Surface((16, 16)))

class ReqSendHuda(NamedTuple):
    request_code: int = 0
    huda: Huda = _duck_huda
    is_mine: bool = True
    taba_code: int = TC_INVALID

compatible_with(obj=ReqSendHuda(), protocol=Request)
