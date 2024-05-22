from typing import Protocol, runtime_checkable

@runtime_checkable
class Notification(Protocol):
    code: int
    message: str