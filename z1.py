from typing import Callable
from functools import partial

MonoFunc = Callable[[], None]

class Ctrl():
    def __init__(self, name: str) -> None:
        self.name = name

    def action(self, func: Callable[[MonoFunc], None]) -> None:
        func(self.callback)

    def callback(self, i: int=0) -> None:
        print(f"{self.name}'s Callback : i={i}")

ccc = Ctrl(name="Controller")

ccc.callback()

def set_i(func: MonoFunc) -> None:
    func(i=100)
    partial(func, i=200)()

ccc.action(set_i)