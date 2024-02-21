import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from math import sin, cos, radians
from typing import Callable, NamedTuple

from mod.const import screen, nie, BRIGHT, BLACK, USAGE_UNUSED, USAGE_USED, TC_SUTEHUDA, HUDA_SCALE
from mod.youso import Youso
from mod.delivery import Delivery
from mod.card import Card, auto_di
from mod.controller import controller
from mod.popup_message import popup_message

def _pass_koudou(delivery: Delivery, hoyuusya: int) -> None:
    pass

class _DrawParams(NamedTuple):
    usage: int = -1
    osame: int = -1

class Huda(Youso):
    def __init__(self, img: Surface, angle: float=0.0, scale: float=HUDA_SCALE, x:int | float=0, y:int | float=0,
                 **kwargs: Callable[..., None]) -> None:
        super().__init__(x=x, y=y, **kwargs)
        self.withdraw: Callable[[], None] = nie(text="Huda.withdraw")
        self.img_nega = img
        self.usage = USAGE_UNUSED
        self.osame = 0
        self.draw_params = _DrawParams()
        self.rearrange(angle=angle, scale=scale, x=x, y=y)
        self.card =  Card(img=Surface((16, 16)), name="", cond=auto_di)
        self.base: 'Huda' = self

    def rotated_verticle(self, x:int | float, y:int | float) -> Vector2:
        rad = radians(-self.angle)
        return Vector2(int(self.x+(cos(rad)*x-sin(rad)*y)*self.scale), int(self.y+(sin(rad)*x+cos(rad)*y)*self.scale))

    def is_cursor_on(self) -> bool:
        inside = False
        mx, my = pygame.mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return inside

    def rearrange(self, angle: float=0.0, scale: float=HUDA_SCALE, x:int | float=0, y:int | float=0) -> bool | None:
        img_intermediate = self.img_nega.copy()
        self.img_rz = pygame.transform.rotozoom(surface=img_intermediate, angle=angle, scale=scale)
        self.angle = angle
        self.scale = scale
        self.x = int(x)
        self.y = int(y)
        self.vertices = [self.rotated_verticle(i[0], i[1]) for i in [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]]
        return None
    
    def redraw(self) -> None:
        self.draw_params = _DrawParams()

    def detail_draw(self) -> None:
        screen.blit(source=self.img_nega, dest=[0, 0])

    def default_draw(self, offset: Vector2 | tuple[int, int] | list[int]=(0, 0)) -> None:
        if self.draw_params != self._draw_params():
            self.draw_params = self._draw_params()
            self._draw_huyo()
        screen.blit(source=self.img_rz, dest=self.img_rz_topleft+offset)

    def shadow_draw(self) -> None:
        pygame.draw.polygon(surface=screen, color=BLACK, points=self.vertices, width=0)
        self.img_rz.set_alpha(192)
        self.default_draw()
        self.img_rz.set_alpha(255)

    def available_draw(self) -> None:
        if controller.hover == self:
            pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in self.vertices], 20)
            self.default_draw(offset=[0, -40])
        else:
            self.default_draw()

    def mousedown(self) -> None:
        controller.active = self

    def play(self) -> None:
        self.card.kaiketu(delivery=self.delivery, hoyuusya=self.hoyuusya, huda=self)

    def can_standard(self, popup: bool=False) -> bool:
        if self.delivery.m_params(self.hoyuusya).played_zenryoku:
            if popup:
                popup_message.add(text=f"既に全力行動しています")
            return False
        elif self.usage == USAGE_USED:
            if popup:
                popup_message.add(text=f"「{self.card.name}」は使用済みです")
            return False
        elif self.card.zenryoku and self.delivery.m_params(self.hoyuusya).played_standard:
            if popup:
                popup_message.add(text=f"既に標準行動しています")
            return False
        elif not self.card.is_full(delivery=self.delivery, hoyuusya=self.hoyuusya):
            if popup:
                popup_message.add(text=f"「{self.card.name}」に費やすフレアが足りません")
            return False
        return True

    def can_play(self, popup: bool=False) -> bool:
        # if self.delivery.m_params(self.hoyuusya).played_zenryoku:
        #     popup_message.add(text=f"既に全力行動しています")
        #     return False
        # elif self.usage == USAGE_USED:
        #     popup_message.add(text=f"「{self.card.name}」は使用済みです")
        #     return False
        # elif self.card.zenryoku and self.delivery.m_params(self.hoyuusya).played_standard:
        #     popup_message.add(text=f"既に標準行動しています")
        #     return False
        # return self.card.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya, popup=popup)
        popup_message.add(f"can_standartは{self.can_standard()}です")
        popup_message.add(f"can_playは{self.card.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya)}です")
        return self.can_standard(popup=popup) and self.card.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya, popup=popup)

    def discard(self) -> None:
        ...
        # if self.card.kirihuda:
        #     self.usage = USAGE_USED
        # else:
        #     self.delivery.send_huda_to_ryouiki(huda=self, is_mine=True, taba_code=TC_SUTEHUDA)

    def _draw_huyo(self) -> None:
        from mod.draw_huyo_functions import draw_huyo
        draw_huyo(self)

    def _draw_params(self) -> _DrawParams:
        return _DrawParams(usage=self.usage, osame=self.osame)

    @property
    def img_rz_topleft(self) -> Vector2:
        return self.dest-Vector2(self.img_rz.get_size())/2
