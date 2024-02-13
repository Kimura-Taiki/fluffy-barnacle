from typing import Callable, Any

from mod.const import pass_func, IMG_TURN_END, IMG_TURN_END_LIGHTEN, POP_START_PHASE_FINISHED
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.ol.button import Button
from mod.moderator import moderator
from mod.youso import Youso
from mod.popup_message import popup_message

class StartPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "開始フェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.button = Button(img_nega=IMG_TURN_END, img_lighten=IMG_TURN_END_LIGHTEN, mouseup=self._mouseup_turn_end)

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        popup_message.add("StartPhase.openへ到着したよ")
        ...

    def close(self) -> PopStat:
        return PopStat(POP_START_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        ...

    def _mouseup_turn_end(self, youso: Youso) -> None:
        moderator.pop()        
