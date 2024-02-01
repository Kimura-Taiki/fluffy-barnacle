from typing import runtime_checkable, Protocol

@runtime_checkable
class Request(Protocol):
    request_code: int
