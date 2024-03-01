#                 20                  40                  60                 79
from pygame import Surface

from mod.const import screen, WX, WY, IMG_GRAY_LAYER, compatible_with, POP_VIEWED_BANMEN, POP_OK, HANTE
from mod.ol.view_banmen import view_youso
from mod.ol.pop_stat import PopStat
from mod.tf.taba_factory import TabaFactory
from mod.classes import Callable, Any, partial, Card, Huda, Taba, Delivery, moderator, popup_message

_HAND_X: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
_HAND_Y_UPPER: Callable[[int, int], float] = lambda i, j: WY/2-150
_HAND_Y_LOWER: Callable[[int, int], float] = lambda i, j: WY-150
_HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0

class OnlySelectLayer():
    def __init__(self, delivery: Delivery, hoyuusya: int=HANTE, name: str="",
    lower: list[Any]=[], upper: list[Any]=[], code: int=POP_OK) -> None:
        self.name = name
        self.inject_func = delivery.inject_view
        self.delivery = delivery
        self.lower = _taba_maid_by_any(li=lower, factory=_factory(os_layer=self
            , huda_y=_HAND_Y_LOWER), delivery=delivery, hoyuusya=hoyuusya)
        self.upper = _taba_maid_by_any(li=upper, factory=_factory(os_layer=self
            , huda_y=_HAND_Y_UPPER), delivery=delivery, hoyuusya=hoyuusya)
        self.select_huda: Huda | None = None
        self.code = code

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.lower.elapse()
        self.upper.elapse()

    def get_hover(self) -> Any | None:
        return self.upper.get_hover_huda() or self.lower.get_hover_huda() or\
            view_youso

    def open(self) -> None:
        popup_message.add(f"{self.name} です")
        if len(self.lower)+len(self.upper) == 0:
            moderator.pop()
        elif len(self.lower) == 1 and len(self.upper) == 0:
            self.lower[0].mouseup()
        elif len(self.lower) == 0 and len(self.upper) == 1:
            self.upper[0].mouseup()

    def close(self) -> PopStat:
        return PopStat(code=self.code, huda=self.select_huda, rest_taba=self.lower)

    def moderate(self, stat: PopStat) -> None:
        if stat.code == POP_VIEWED_BANMEN:
            return
        moderator.pop()

def _mouseup(huda: Huda, os_layer: OnlySelectLayer) -> None:
    os_layer.select_huda = huda
    huda.withdraw()
    moderator.pop()

def _factory(os_layer: OnlySelectLayer, huda_y: Callable[[int, int], float]
) -> TabaFactory:
    facotry = TabaFactory(inject_kwargs={"mouseup": partial(_mouseup,
        os_layer=os_layer)}, huda_x=_HAND_X, huda_y=huda_y, huda_angle=
        _HAND_ANGLE, is_ol=True)
    return facotry

def _taba_maid_by_any(li: list[Any], factory: TabaFactory, delivery: Delivery,
hoyuusya: int) -> Taba:
    if len(li) == 0:
        return Taba()
    elif isinstance(li[0], Surface):
        return factory.maid_by_files(surfaces=li, hoyuusya=hoyuusya)
    elif isinstance(li[0], Huda):
        return factory.maid_by_hudas(hudas=li, hoyuusya=hoyuusya)
    elif isinstance(li[0], Card):
        return factory.maid_by_cards(cards=li, delivery=delivery, hoyuusya=
                                     hoyuusya)
    else:
        raise ValueError("要素群が適切ではありません", li)

# compatible_with(, OverLayer)
        

