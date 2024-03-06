#                 20                  40                  60                 79
from mod.const import compatible_with, pass_func, IMG_TURN_END, IMG_TURN_END_LIGHTEN, POP_MAIN_PHASE_FINISHED
from mod.classes import Callable, PopStat, Youso, moderator
from mod.ol.over_layer import OverLayer
from mod.delivery import Delivery, duck_delivery
from mod.ol.button import Button

class MainPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "メインフェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player
        self.button = Button(img_nega=IMG_TURN_END, img_lighten=IMG_TURN_END_LIGHTEN, mouseup=self._mouseup_turn_end)

    def elapse(self) -> None:
        self.button.draw()

    def get_hover(self) -> Youso | None:
        return self.button if self.button.is_cursor_on() else None

    def open(self) -> None:
        ...

    def close(self) -> PopStat:
        return PopStat(POP_MAIN_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        ...

    def _mouseup_turn_end(self, youso: Youso) -> None:
        moderator.pop()        

compatible_with(MainPhase(), OverLayer)