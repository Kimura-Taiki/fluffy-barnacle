from typing import Protocol, runtime_checkable

from ptc.notification import Notification

@runtime_checkable
class Listener(Protocol):
    def listen(self, nf: Notification) -> None:
        ...