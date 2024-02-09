#                 20                  40                  60                 79
from pygame.math import Vector2
from typing import Any, Callable

from mod.const import compatible_with, pass_func, PH_NONE, PH_MAIN
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Kougeki
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery, duck_delivery
from mod.ol.uke_taba import make_uke_taba
from mod.ol.taiou_taba import make_taiou_taba
from mod.ol.main_phase import MainPhase
from mod.ol.over_layer import OverLayer

class TurnProgression():
    def __init__(self, delivery: Delivery, main_inject: Callable[[], None]) -> None:
        self.name = "1ターン目 下手"
        self.inject_func: Callable[[], None] = pass_func
        self.main_inject = main_inject
        self.phase = PH_NONE
        self.delivery: Delivery = delivery

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        moderator.append(MainPhase(inject_func=self.main_inject))

    def close(self) -> Any:
        ...

    def moderate(self, stat: int) -> None:
        ...

compatible_with(TurnProgression(delivery=duck_delivery, main_inject=pass_func), OverLayer)
