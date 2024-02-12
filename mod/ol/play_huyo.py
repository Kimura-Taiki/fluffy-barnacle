#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.transform import scale
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, IMG_DECISION, IMG_DECISION_LIGHTEN,\
    IMG_OSAME_DUST, IMG_OSAME_DUST_LIGHTEN, IMG_OSAME_AURA, IMG_OSAME_AURA_LIGHTEN, draw_aiharasuu,\
    FONT_SIZE_OSAME_NUM, UC_DUST, UC_AURA
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
        self.button_dust = Button(
            img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN,
            x=WX/2-110, y=WY/2-150, mouseup=self._mouseup_dust_shift)
        self.button_aura = Button(
            img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN,
            x=WX/2+110, y=WY/2-150, mouseup=self._mouseup_aura_shift)
        self.osame = card.osame(delivery, hoyuusya)
        self.dust_num = delivery.ouka_count(hoyuusya=hoyuusya, is_mine=False, utuwa_code=UC_DUST)
        self.aura_num = delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_AURA)
        self.dust_osame = min(self.dust_num, self.osame)
        self.aura_osame = min(self.aura_num, self.osame-self.dust_osame)
        self._rearrange()
        self.button_decision = Button(img_nega=IMG_DECISION, img_lighten=IMG_DECISION_LIGHTEN)
        self.buttons = [self.button_dust, self.button_aura, self.button_decision]

    def _rearrange(self) -> None:
        _rearrange_button(button=self.button_dust, img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN, num=self.dust_osame)
        _rearrange_button(button=self.button_aura, img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN, num=self.aura_osame)

    def elapse(self) -> None:
        screen.blit(source=self.card.img, dest=-Vector2(self.card.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        for button in self.buttons:
            button.draw()

    def get_hover(self) -> Any | None:
        return next((button for button in self.buttons if button.is_cursor_on()), view_youso)

    def open(self) -> None:
        ...

    def close(self) -> int:
        popup_message.add("解決した！？")
        self.card.close(hoyuusya=self.hoyuusya)
        return 0

    def moderate(self, stat: Any) -> None:
        ...

    def _mouseup_dust_shift(self, huda: Huda) -> None:
        if self.aura_osame > 0 and self.dust_num-self.dust_osame > 0:
            self.dust_osame += 1
            self.aura_osame -= 1
            self._rearrange()

    def _mouseup_aura_shift(self, huda: Huda) -> None:
        if self.dust_osame > 0 and self.aura_num-self.aura_osame > 0:
            self.aura_osame += 1
            self.dust_osame -= 1
            self._rearrange()

def _rearrange_button(button: Button, img_nega: Surface, img_lighten: Surface, num: int) -> None:
    button.img_nega = _img_in_number(img_base=img_nega, num=num)
    button.img_lighten = _img_in_number(img_base=img_lighten, num=num)

def _img_in_number(img_base: Surface, num: int) -> Surface:
    img_return = img_base.copy()
    draw_aiharasuu(surface=img_return, dest=Vector2(img_return.get_size())/2-
                    [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=num, size=FONT_SIZE_OSAME_NUM)
    return img_return

# compatible_with(, OverLayer)
