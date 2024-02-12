#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.transform import scale
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, IMG_DECISION, IMG_DECISION_LIGHTEN,\
    IMG_OSAME_DUST, IMG_OSAME_DUST_LIGHTEN, IMG_OSAME_AURA, IMG_OSAME_AURA_LIGHTEN, draw_aiharasuu, FONT_SIZE_OSAME_NUM
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.button import Button

class PlayHuyo():
    def __init__(self, card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.card = card
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"付与:{card.name}の使用"
        self.inject_func = delivery.inject_view
        self.button_dust = Button(img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN, x=WX/2-110, y=WY/2-150)
        self.button_aura = Button(img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN, x=WX/2+110, y=WY/2-150)
        self.dust_num = 2
        self.aura_num = 0
        self._rearrange_button(button=self.button_dust, img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN, num=self.dust_num)
        self._rearrange_button(button=self.button_aura, img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN, num=self.aura_num)
        self.button_decision = Button(img_nega=IMG_DECISION, img_lighten=IMG_DECISION_LIGHTEN)
        self.buttons = [self.button_dust, self.button_aura, self.button_decision]

    def _rearrange_button(self, button: Button, img_nega: Surface, img_lighten: Surface, num: int) -> None:
        button.img_nega = img_nega.copy()
        draw_aiharasuu(surface=button.img_nega, dest=Vector2(button.img_nega.get_size())/2-
                       [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=num, size=FONT_SIZE_OSAME_NUM)
        button.img_lighten = img_lighten.copy()
        draw_aiharasuu(surface=button.img_lighten, dest=Vector2(button.img_lighten.get_size())/2-
                       [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=num, size=FONT_SIZE_OSAME_NUM)

    def elapse(self) -> None:
        screen.blit(source=self.card.img, dest=-Vector2(self.card.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        for button in self.buttons:
            button.draw()

    def get_hover(self) -> Any | None:
        # return self.button if self.button.is_cursor_on() else view_youso
        return next((button for button in self.buttons if button.is_cursor_on()), view_youso)

    def open(self) -> None:
        ...

    def close(self) -> int:
        popup_message.add("解決した！？")
        self.card.close(hoyuusya=self.hoyuusya)
        return 0

    def moderate(self, stat: Any) -> None:
        ...

# compatible_with(, OverLayer)
