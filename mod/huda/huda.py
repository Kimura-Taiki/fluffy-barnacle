#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable

from mod.const import nie, USAGE_UNUSED, USAGE_DEPLOYED, USAGE_USED, HUDA_SCALE
from mod.youso import Youso
from mod.card.card import Card, auto_di
from mod.controller import controller
from mod.popup_message import popup_message
from mod.huda.draw_params import DrawParams
from mod.huda.huda_draw import HudaDraw
from mod.card.card_func import is_meet_conditions

class Huda(Youso):
    def __init__(self, img: Surface=Surface((16, 16)), angle: float=0.0, scale: float=HUDA_SCALE, x:int | float=0, y:int | float=0,
                 **kwargs: Callable[..., None]) -> None:
        super().__init__(x=x, y=y, **kwargs)
        self.withdraw: Callable[[], None] = nie(text="Huda.withdraw")
        self.usage = USAGE_UNUSED
        self.osame = 0
        self.draw_params = DrawParams()
        self._card =  Card(img=Surface((16, 16)), name="", cond=auto_di)
        self.base: 'Huda' = self
        self.huda_draw = HudaDraw(img=img, x=x, y=y, angle=angle, scale=scale, update_func=self._update_func, huda=self)
        self.rearrange(angle=angle, scale=scale, x=x, y=y)

    def is_cursor_on(self) -> bool:
        return self.huda_draw.is_cursor_on()

    def rearrange(self, angle: float=0.0, scale: float=HUDA_SCALE, x:int | float=0, y:int | float=0) -> bool | None:
        self.angle = angle
        self.x = int(x)
        self.y = int(y)
        self.huda_draw.rearrange(x=x, y=y, angle=angle, scale=scale)
        return None

    def _update_func(self, huda_draw: HudaDraw) -> None:
        if self.draw_params == (dp := DrawParams.made_by_huda(huda=self)):
            return
        self.draw_params = dp
        self.rearrange(angle=self.angle, x=self.x, y=self.y)

    def detail_draw(self) -> None:
        self.huda_draw.detail_draw()

    def default_draw(self, offset: Vector2 | tuple[int, int] | list[int]=(0, 0)) -> None:
        self.huda_draw.default_draw(offset=offset)

    def shadow_draw(self) -> None:
        self.huda_draw.shadow_draw()

    def available_draw(self) -> None:
        self.huda_draw.available_draw()

    def mousedown(self) -> None:
        controller.active = self

    def play(self) -> None:
        self.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya, huda=self)

    def can_standard(self, popup: bool = False, is_zenryoku: bool = False) -> bool:
        checks: list[tuple[bool, str]] = [
            (self.delivery.m_params(self.hoyuusya).played_zenryoku, "既に全力行動しています"),
            (self.delivery.m_params(self.hoyuusya).played_syuutan, "既に終端行動しています"),
            (is_zenryoku and self.card.zenryoku and self.delivery.m_params(self.hoyuusya).played_standard, "既に標準行動しています"),
            (self.usage == USAGE_DEPLOYED, f"「{self.card.name}」は展開中です"),
            (self.usage == USAGE_USED, f"「{self.card.name}」は使用済みです"),
            (not self.card.is_full(delivery=self.delivery, hoyuusya=self.hoyuusya), f"「{self.card.name}」に費やすフレアが足りません")
        ]
        return is_meet_conditions(checks=checks, popup=popup)

    def can_play(self, popup: bool=False) -> bool:
        return self.can_standard(popup=popup) and self.card.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya, popup=popup)

    @property
    def card(self) -> Card:
        return self._card

    @card.setter
    def card(self, card: Card) -> None:
        self._card = card