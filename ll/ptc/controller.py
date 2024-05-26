from typing import runtime_checkable, Protocol

@runtime_checkable
class Controller(Protocol):
    def action(self) -> None:
        ...

    def callback(self) -> None:
        ...