import pygame
from pygame.surface import Surface
from typing import Callable, Protocol, Any, runtime_checkable

from mod.const import pass_func, MS_MINCHO_COL, WHITE, BLACK, screen, FONT_SIZE_STACK_LOG
from mod.delivery import Delivery, duck_delivery
from mod.ol.over_layer import OverLayer
from mod.popup_message import popup_message

class Moderator():
    def __init__(self) -> None:
        self.stack: list[OverLayer] = []
        self.inject_funcs: Callable[[], None] = pass_func
        self.delivery: Delivery = duck_delivery

    def append(self, over_layer: OverLayer) -> None:
        over_layer.delivery = self.delivery
        self.stack.append(over_layer)
        popup_message.add(text=f"{over_layer.name} を開きます")
        over_layer.inject_func()
        over_layer.open()

    def pop(self) -> None:
        over_layer = self.stack.pop()
        self.stack[-1].inject_func()
        popup_message.add(text=f"{over_layer.name} を閉じます")
        self.stack[-1].moderate(stat=over_layer.close())
        # popup_message.add(text=f"{over_layer.name} のpopが終わる")

    def get_hover(self) -> Any | None:
        return self.stack[-1].get_hover()

    def elapse(self) -> None:
        self.stack[-1].elapse()

    def stack_log(self) -> None:
        img_nega = Surface((340, (FONT_SIZE_STACK_LOG+4)*len(self.stack)), pygame.SRCALPHA)
        for i, v in enumerate(self.stack):
            mozi = MS_MINCHO_COL(" "*i+v.name, 20, BLACK)
            siro = Surface(mozi.get_size())
            siro.fill(WHITE)
            siro.set_alpha(192)
            img_nega.blit(source=siro, dest=[0, i*(FONT_SIZE_STACK_LOG+4)])
            img_nega.blit(source=mozi, dest=[0, i*(FONT_SIZE_STACK_LOG+4)])
        screen.blit(source=img_nega, dest=[0, 0])

moderator = Moderator()