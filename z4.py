from copy import deepcopy
from dataclasses import dataclass, field
from pygame import Surface
from time import sleep
from typing import Callable, Protocol, runtime_checkable

@dataclass
class View:
    image: Surface = field(default_factory=lambda : Surface((16, 16)))

@dataclass
class Router:
    hooks: list[Callable[[], None]] = field(default_factory=list)

@dataclass
class Model:
    game_params: list[int] = field(default_factory=list)
    router: Router = field(default_factory=Router)

    def resolve_hooks(self) -> None:
        print("非同期処理のテスト")
        for hook in self.router.hooks:
            hook()

@dataclass
class Bridge:
    view: View
    model: Model

@runtime_checkable
class Controller(Protocol):
    bridge: Bridge

    def async_func(self) -> None:
        ...

@dataclass
class Ctrl1:
    bridge: Bridge

    def async_func(self) -> None:
        sleep(0.1)
        print("async_funcの１号だよ")

@dataclass
class Ctrl2:
    bridge: Bridge

    def async_func(self) -> None:
        sleep(0.4)
        print("async_func２号です")

@dataclass
class Ctrl3:
    bridge: Bridge

    def async_func(self) -> None:
        sleep(0.9)
        print("async_funcヶ３号也")


vv = View()
mm = Model()
bb = Bridge(view=vv, model=mm)
rr = Router(hooks=[
    Ctrl1(bb).async_func,
    Ctrl2(bb).async_func,
    Ctrl3(bb).async_func
])
empty_rr = Router()
mm.router = rr

mm.resolve_hooks()

mm.router = empty_rr
copy_mm = deepcopy(mm)
print("コピーしたよ")
copy_mm.router = rr

copy_mm.resolve_hooks()