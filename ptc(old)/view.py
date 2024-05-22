from typing import Protocol, runtime_checkable

@runtime_checkable
class View(Protocol):
    def draw(self) -> None:
        ...
