#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2

from mod.const import screen, IMG_SYUUTYUU_AREA, ACTION_CIRCLE_NEUTRAL,\
    ACTION_CIRCLE_YADOSI, ACTION_CIRCLE_BASIC, ACTION_CIRCLE_ZENSIN,\
    pass_func, BRIGHT
from mod.classes import Callable, Card, controller, popup_message
from mod.mkt.utuwa import Utuwa
from mod.kihondousa import zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card
from mod.ol.others_basic_action import obal_func

def _mousedown(utuwa: Utuwa) -> None:
    if utuwa.osame == 0:
        popup_message.add("集中力が0です")
        return
    controller.active = utuwa
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def _active(utuwa: Utuwa) -> None:
    # huda.detail_draw()
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        # controller.data_transfer = utuwa
        controller.active = None
    else:
        # source = {3: ACTION_CIRCLE_CARD, 2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
        source = {3: ACTION_CIRCLE_NEUTRAL, 2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
            int((diff_coord.angle_to([0, 0])+225)/90), ACTION_CIRCLE_ZENSIN)
        screen.blit(source=source, dest=controller.hold_coord-[250, 250])

_yadosi = obal_func(cards=[yadosi_card])
_basic = obal_func(cards=[zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card], text="その他基本動作です")
_zensin = obal_func(cards=[zensin_card])
# _use_card: Callable[[Card], Callable[[Huda], None]] = lambda card: obal_func(cards=[card], text=f"手札から「{card.name}」カードを使います", mode=OBAL_USE_CARD)

def _no_card(utuwa: Utuwa) -> None:
    popup_message.add("集中力はカードではありません")

def _mouseup(utuwa: Utuwa) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50: return
    # {3: _use_card(huda.card), 2: _yadosi, 1: _basic}.get(int((diff_coord.angle_to([0, 0])+225)/90), _zensin)(huda)
    {3: _no_card, 2: _yadosi, 1: _basic}.get(int((diff_coord.angle_to([0, 0])+225)/90), _zensin)(utuwa)

def syuutyuu_utuwa(hoyuusya: int, osame: int, x: int, y: int) -> Utuwa:
#                 20                  40                  60                 79
    return Utuwa(
        img=IMG_SYUUTYUU_AREA, hoyuusya=hoyuusya, osame=osame, x=x, y=y, max=2,
        mousedown=_mousedown, active=_active, mouseup=_mouseup)


# self.syuutyuu = Utuwa(img=IMG_SYUUTYUU_AREA, hoyuusya=self.hoyuusya, osame=0, x=310, y=WY-210, max=2)
