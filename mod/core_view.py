from typing import Protocol, runtime_checkable

from mod.huda import Huda

@runtime_checkable
class CoreView(Protocol):
    def elapse(self) -> None:
        ...

    def get_hover_huda(self) -> Huda | None:
        ...

    def text(self, name: str) -> str:
        ...