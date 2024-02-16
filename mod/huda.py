import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from math import sin, cos, radians
from typing import Callable

from mod.const import screen, nie, BRIGHT, BLACK, USAGE_UNUSED, USAGE_DEPLOYED, USAGE_USED, IMG_OSAME, TC_SUTEHUDA,\
    HUDA_SCALE, draw_aiharasuu
from mod.youso import Youso
from mod.delivery import Delivery
from mod.kihondousa import pass_koudou
from mod.card import Card, auto_di
from mod.controller import controller
from mod.popup_message import popup_message

class Huda(Youso):
    def __init__(self, img: Surface, angle: float=0.0, scale: float=HUDA_SCALE, x:int | float=0, y:int | float=0,
                 **kwargs: Callable[..., None]) -> None:
        super().__init__(x=x, y=y, **kwargs)
        self.withdraw: Callable[[], None] = nie(text="Huda.withdraw")
        self.img_nega = img
        self.usage = USAGE_UNUSED
        self.osame = 0
        self._pre_osame = 0
        self.rearrange(angle=angle, scale=scale, x=x, y=y)
        self.koudou: Callable[[Delivery, int], None] = pass_koudou
        self.card =  Card(img=Surface((16, 16)), name="", cond=auto_di)

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
        # from mod.const import MS_MINCHO_COL, side_name
        # img_intermediate.blit(source=MS_MINCHO_COL(side_name(self.hoyuusya), 64, (0, 0, 0)), dest=(0, 200))
        if self.usage == USAGE_DEPLOYED:
            img_intermediate.blit(source=IMG_OSAME, dest=[0, 0])
            draw_aiharasuu(surface=img_intermediate, dest=Vector2(5, 0), num=self.osame)
        self.img_rz = pygame.transform.rotozoom(surface=img_intermediate, angle=angle, scale=scale)
        self.angle = angle
        self.scale = scale
        self.x = int(x)
        self.y = int(y)
        self.vertices = [self.rotated_verticle(i[0], i[1]) for i in [[-170.0, -237.5], [170.0, -237.5], [170.0, 237.5], [-170.0, 237.5]]]
        return None

    def detail_draw(self) -> None:
        screen.blit(source=self.img_nega, dest=[0, 0])

    def default_draw(self, offset: Vector2 | tuple[int, int] | list[int]=(0, 0)) -> None:
        if self.osame != self._pre_osame:
            self.rearrange(x=self.x, y=self.y, angle=self.angle)
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

    def can_play(self) -> bool:
        if self.usage == USAGE_USED:
            popup_message.add(text=f"「{self.card.name}」は使用済みです")
            return False
        return self.card.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya)

    def discard(self) -> None:
        if self.card.kirihuda:
            self.usage = USAGE_USED
        else:
            self.delivery.send_huda_to_ryouiki(huda=self, is_mine=True, taba_code=TC_SUTEHUDA)

    @property
    def img_rz_topleft(self) -> Vector2:
        return self.dest-Vector2(self.img_rz.get_size())/2
