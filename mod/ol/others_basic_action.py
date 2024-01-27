import pygame
from typing import Protocol, Callable, Any

from mod.const import compatible_with, WX, WY
from mod.moderator import OverLayer
from mod.huda import default_draw
from mod.taba import Taba
from mod.taba_factory import TabaFactory

HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-110*(j-1)+220*i
HAND_Y: Callable[[int, int], float] = lambda i, j: WY/2
HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0

_basic_action_factory = TabaFactory(inject_kwargs={"draw": default_draw}, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
_card_list = [pygame.image.load(f"pictures/{i}.png").convert_alpha() for i in [
    "kihon_zensin", "kihon_ridatu", "kihon_koutai", "kihon_matoi", "kihon_yadosi"]]
ba_taba = _basic_action_factory.maid_by_files(surfaces=_card_list, )

class OthersBasicAction(Protocol):
    inject_func: Callable[[], None]

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        

    def close(self) -> int:
        ...

    def moderate(self, stat: int) -> None:
        ...

compatible_with(OthersBasicAction(), OverLayer)