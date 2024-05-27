from typing import runtime_checkable, Protocol, Any

@runtime_checkable
class Controller(Protocol):
    def action(self) -> None:
        ...
