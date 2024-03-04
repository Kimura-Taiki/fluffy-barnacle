#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.transform import scale
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, IMG_DECISION, IMG_DECISION_LIGHTEN,\
    IMG_OSAME_DUST, IMG_OSAME_DUST_LIGHTEN, IMG_OSAME_AURA, IMG_OSAME_AURA_LIGHTEN, draw_aiharasuu,\
    FONT_SIZE_OSAME_NUM, UC_DUST, UC_AURA, USAGE_DEPLOYED, POP_OK, POP_OPEN, enforce, IMG_DONOR_DUST, IMG_DONOR_AURA
from mod.classes import Any, PopStat, Card, Youso, Huda, Delivery, moderator,\
    popup_message
from mod.ol.view_banmen import view_youso
from mod.mkt.utuwa import Utuwa
from mod.ol.button import Button
from mod.tf.taba_factory import TabaFactory
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

class _Donor():
    def __init__(self, name: str, youso: Youso, img: Surface) -> None:
        self.name = name
        self.youso = youso
        self.img_nega = img
        self.donation = 0

    def img(self) -> Surface:
        img_return = self.img_nega.copy()
        draw_aiharasuu(surface=img_return, dest=Vector2(img_return.get_size())/2-
                        [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=self.donation, size=FONT_SIZE_OSAME_NUM)
        return img_return

    def pour(self, amount: int) -> int:
        if amount <= 0:
            return amount
        self.donation = min(amount, self.youso.osame)
        return amount-self.donation

def _youso(layer: PipelineLayer, utuwa_code: int) -> Youso:
    return enforce(layer.delivery.utuwa_target(hoyuusya=layer.hoyuusya,
        is_mine=True, utuwa_code=utuwa_code), Youso)

def _donors(layer: PipelineLayer, amount: int) -> list[_Donor]:
    dust_doner = _Donor(name="ダスト", youso=_youso(layer, UC_DUST),
                        img=IMG_DONOR_DUST)
    aura_doner = _Donor(name="オーラ", youso=_youso(layer, UC_AURA),
                        img=IMG_DONOR_AURA)
    amount = dust_doner.pour(amount=amount)
    amount = aura_doner.pour(amount=amount)
    return [dust_doner, aura_doner]
#                 20                  40                  60                 79

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    # moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
    #     hoyuusya, name="納の供出元の選択", upper=[enforce(donor, _Donor).img() for
    #     donor in layer.rest], code=code))
    moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
        hoyuusya, name="納の供出元の選択",
        upper=list(TabaFactory().maid_by_tuples(tuples=[(enforce(donor, _Donor).
        name, enforce(donor, _Donor).img()) for donor in layer.rest], delivery=
        layer.delivery, hoyuusya=layer.hoyuusya)), code=code))

def play_huyo_layer(card: Card, delivery: Delivery, hoyuusya: int,
                    huda: Any | None, code: int=POP_OK) -> PipelineLayer:
#                 20                  40                  60                 79
    hd = enforce(huda, Huda)
    layer = PipelineLayer(name=f"付与:{hd.card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_OPEN)
        }, huda=huda, code=code)
    layer.rest = _donors(layer, card.osame(delivery, hoyuusya))
    return layer


# class PlayHuyo():
#     def __init__(self, card: Card, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int=POP_OK) -> None:
#         self.card = card
#         if not isinstance(huda, Huda):
#             raise ValueError(f"Invalid huda: {huda}")
#         self.huda = huda
#         self.delivery = delivery
#         self.hoyuusya = hoyuusya
#         self.source_huda = huda if isinstance(huda, Huda) else None
#         self.name = f"付与:{card.name}の使用"
#         self.inject_func = delivery.inject_view
#         self.button_dust = Button(
#             img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN,
#             x=WX/2-110, y=WY/2-150, mouseup=self._mouseup_dust_shift)
#         self.button_aura = Button(
#             img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN,
#             x=WX/2+110, y=WY/2-150, mouseup=self._mouseup_aura_shift)
#         self.osame = card.osame(delivery, hoyuusya)
#         self.dust_num = delivery.ouka_count(hoyuusya=hoyuusya, is_mine=False, utuwa_code=UC_DUST)
#         self.aura_num = delivery.ouka_count(hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_AURA)
#         self.dust_osame = min(self.dust_num, self.osame)
#         self.aura_osame = min(self.aura_num, self.osame-self.dust_osame)
#         self._rearrange()
#         self.button_decision = Button(
#             img_nega=IMG_DECISION, img_lighten=IMG_DECISION_LIGHTEN, mouseup=self._mouseup_decision)
#         self.buttons = [self.button_dust, self.button_aura, self.button_decision]
#         self.code = code

#     def _rearrange(self) -> None:
#         _rearrange_button(button=self.button_dust, img_nega=IMG_OSAME_DUST, img_lighten=IMG_OSAME_DUST_LIGHTEN, num=self.dust_osame)
#         _rearrange_button(button=self.button_aura, img_nega=IMG_OSAME_AURA, img_lighten=IMG_OSAME_AURA_LIGHTEN, num=self.aura_osame)

#     def elapse(self) -> None:
#         screen.blit(source=self.card.img, dest=-Vector2(self.card.img.get_size())/2+Vector2(WX, WY)/2)
#         screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
#         for button in self.buttons:
#             button.draw()

#     def get_hover(self) -> Any | None:
#         return next((button for button in self.buttons if button.is_cursor_on()), view_youso)

#     def open(self) -> None:
#         ...

#     def close(self) -> PopStat:
#         self.card.close(hoyuusya=self.hoyuusya)
#         return PopStat(self.code, self.source_huda)

#     def moderate(self, stat: PopStat) -> None:
#         ...

#     def _mouseup_dust_shift(self, youso: Youso) -> None:
#         if self.aura_osame > 0 and self.dust_num-self.dust_osame > 0:
#             self.dust_osame += 1
#             self.aura_osame -= 1
#             self._rearrange()

#     def _mouseup_aura_shift(self, youso: Youso) -> None:
#         if self.dust_osame > 0 and self.aura_num-self.aura_osame > 0:
#             self.aura_osame += 1
#             self.dust_osame -= 1
#             self._rearrange()

#     def _mouseup_decision(self, youso: Youso) -> None:
#         self.delivery.send_ouka_to_ryouiki(hoyuusya=self.hoyuusya,
#             from_mine=False, from_code=UC_DUST, to_huda=self.huda, kazu=self.dust_osame)
#         self.delivery.send_ouka_to_ryouiki(hoyuusya=self.hoyuusya,
#             from_mine=True, from_code=UC_AURA, to_huda=self.huda, kazu=self.aura_osame)
#         self.huda.usage = USAGE_DEPLOYED
#         moderator.pop()

# def _rearrange_button(button: Button, img_nega: Surface, img_lighten: Surface, num: int) -> None:
#     button.img_nega = _img_in_number(img_base=img_nega, num=num)
#     button.img_lighten = _img_in_number(img_base=img_lighten, num=num)

# def _img_in_number(img_base: Surface, num: int) -> Surface:
#     img_return = img_base.copy()
#     draw_aiharasuu(surface=img_return, dest=Vector2(img_return.get_size())/2-
#                     [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=num, size=FONT_SIZE_OSAME_NUM)
#     return img_return

# # compatible_with(, OverLayer)
