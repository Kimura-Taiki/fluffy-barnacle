from typing import Protocol, Callable
from functools import partial


def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(text)
    return raise_func


class Hoge:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.method: Callable[[], None] = nie(text="Hoge.method が未実装です")


class Duck(Protocol):
    def method(self) -> None:
        ...


def _method_hoge(hoge: Hoge) -> None:
    print(f"Hoge({hoge.x}, {hoge.y})")


def call_duck(duck: Duck) -> None:
    duck.method()


hoge = Hoge(x=10, y=35)
hoge.method()
hoge.method = partial(_method_hoge, hoge=hoge)
call_duck(duck=hoge)
