#                 20                  40                  60                 79
from mod.const import screen, WX, WY, IMG_GRAY_LAYER, compatible_with, POP_VIEWED_BANMEN, POP_OK
from mod.ol.view_banmen import view_youso
from mod.ol.pop_stat import PopStat
from mod.tf.taba_factory import TabaFactory
from mod.classes import Callable, Any, Huda, Taba, Delivery, moderator, popup_message

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_Y_UPPER: Callable[[int, int], float] = lambda i, j: WY/2-150
HAND_Y_LOWER: Callable[[int, int], float] = lambda i, j: WY-150

class OnlySelectLayer():
    def __init__(self, delivery: Delivery, name: str="", taba: Taba=Taba(),
                 code: int=POP_OK) -> None:
        self.name = name
        self.inject_func = delivery.inject_view
        self.delivery = delivery
        self.taba = taba
        self.select_huda: Huda | None = None
        self.code = code

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        # self.taba.elapse()

    def get_hover(self) -> Any | None:
        return self.taba.get_hover_huda() or view_youso

    def open(self) -> None:
        # popup_message.add(f"{self.name} です")
        # if not self.taba:
        #     moderator.pop()
        # elif len(self.taba) == 1:
        #     self.taba[0].mouseup()
        ...

    def close(self) -> PopStat:
        return PopStat(code=self.code, huda=self.select_huda, rest_taba=self.taba)

    def moderate(self, stat: PopStat) -> None:
        if stat.code == POP_VIEWED_BANMEN:
            return
        moderator.pop()

def mouseup(huda: Huda, os_layer: OnlySelectLayer) -> None:
    os_layer.select_huda = huda
    os_layer.taba.remove(huda)
    moderator.pop()

# compatible_with(, OverLayer)
        

