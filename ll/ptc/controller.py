from typing import runtime_checkable, Protocol, Callable

@runtime_checkable
class Controller(Protocol):
    def action(self) -> None:
        ...

    def callback(self) -> None:
        ...