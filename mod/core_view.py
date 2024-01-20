from typing import Protocol

from mod.huda import Huda
# from mod.taba import Taba
# from mod.delivery import Delivery

class CoreView(Protocol):
    def elapse(self) -> None:
        ...

    def rearrange(self) -> None:
        ...

    def get_hover_huda(self) -> Huda | None:
        ...