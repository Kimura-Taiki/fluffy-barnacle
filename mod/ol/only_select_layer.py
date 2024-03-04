#                 20                  40                  60                 79
from pygame import Surface, SRCALPHA
from pygame.math import Vector2

from mod.const import screen, WX, WY, IMG_GRAY_LAYER, compatible_with, POP_OK,\
    POP_VIEWED_BANMEN, HANTE, MS_MINCHO_COL, FONT_SIZE_TITLE, WHITE, BLACK, pass_func, IMG_DECISION, POP_DECIDED
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
    lower: list[Any]=[], upper: list[Any]=[], decide: bool=False,
    popup: bool=True, code: int=POP_OK) -> None:
        self.name = name
        self.img_title = _img_title(text=name)
        self.inject_func = delivery.inject_view
        self.delivery = delivery
        self.lower = _taba_maid_by_any(li=lower, factory=_factory(os_layer=self
            , huda_y=_HAND_Y_LOWER), delivery=delivery, hoyuusya=hoyuusya)
        self.upper = _taba_maid_by_any(li=upper, factory=_factory(os_layer=self
            , huda_y=_HAND_Y_UPPER, is_detail=False), delivery=delivery,
            hoyuusya=hoyuusya)
        self.decide = _decide(decide, self)
        self.select_huda: Huda | None = None
        self.popup = popup
        self.code = code

    def elapse(self) -> None:
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        screen.blit(source=self.img_title, dest=[WX/2-self.img_title.get_width()/2, 0])
        self.lower.elapse()
        self.upper.elapse()
        self.decide.draw()

    def get_hover(self) -> Any | None:
        return self.upper.get_hover_huda() or self.lower.get_hover_huda() or\
            (self.decide if self.decide.is_cursor_on() else view_youso)

    def open(self) -> None:
        if len(self.lower)+len(self.upper) == 0:
            moderator.pop()
        elif len(self.lower) == 1 and len(self.upper) == 0:
            self.lower[0].mouseup()
        elif len(self.lower) == 0 and len(self.upper) == 1:
            self.upper[0].mouseup()
        else:
            if self.popup:
                popup_message.add(f"{self.name} です")

    def close(self) -> PopStat:
        return PopStat(code=self.code, huda=self.select_huda, rest_taba=self.lower)

    def moderate(self, stat: PopStat) -> None:
        if stat.code == POP_VIEWED_BANMEN:
            return
        moderator.pop()

def _mouseup_decide(huda: Huda, os_layer: OnlySelectLayer) -> None:
    os_layer.select_huda = huda
    os_layer.code = POP_DECIDED
    huda.withdraw()
    moderator.pop()

def _decide(is_decide: bool, os_layer: OnlySelectLayer) -> Huda:
    img = IMG_DECISION
    coord = Vector2(WX, WY)*(1 if is_decide else 2)-Vector2(img.get_size())/2
    print(is_decide, coord, img, os_layer)
    return Huda(img=img, x=coord.x, y=coord.y, draw=Huda.available_draw, mouseup=lambda huda: _mouseup_decide(huda, os_layer))

def _img_title(text: str) -> Surface:
    kuro = MS_MINCHO_COL(text, FONT_SIZE_TITLE, BLACK)
    siro = MS_MINCHO_COL(text, FONT_SIZE_TITLE, WHITE)
    bg = Surface(Vector2(64, 0)+kuro.get_size(), SRCALPHA)
    bg.fill(WHITE)
    bg.set_alpha(192)
    print(bg.get_size())
    img = Surface(bg.get_size(), SRCALPHA)
    img.blit(source=bg, dest=[0, 0])
    for tpl in [(32-2, 0), (32, -2), (32+2, 0), (32, 2)]:
        img.blit(source=siro, dest=tpl)
    img.blit(source=kuro, dest=[32, 0])
    return img

def _mouseup(huda: Huda, os_layer: OnlySelectLayer) -> None:
    os_layer.select_huda = huda
    huda.withdraw()
    moderator.pop()

def _factory(os_layer: OnlySelectLayer, huda_y: Callable[[int, int], float],
is_detail: bool=True) -> TabaFactory:
#                 20                  40                  60                 79
    inject: dict[str, Callable[[Huda], None]] = {"mouseup": partial(_mouseup,
        os_layer=os_layer)} | ({} if is_detail else {"hover": pass_func})
    facotry = TabaFactory(inject_kwargs=inject, huda_x=_HAND_X, huda_y=huda_y,
                          huda_angle=_HAND_ANGLE, is_ol=True)
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
        

