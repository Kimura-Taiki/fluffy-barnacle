from typing import NamedTuple, Any

from mod.const import POP_OK

class PopStat(NamedTuple):
    code: int = POP_OK
    huda: Any | None = None
    card: Any | None = None
    rest_taba: list[Any] = []
    switch: bool = False