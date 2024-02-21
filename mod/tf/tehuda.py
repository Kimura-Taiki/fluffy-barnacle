#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, BRIGHT, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_CARD, ACTION_CIRCLE_BASIC \
    , ACTION_CIRCLE_ZENSIN, ACTION_CIRCLE_YADOSI, TC_HUSEHUDA, OBAL_KIHONDOUSA, OBAL_USE_CARD
from mod.huda import Huda
from mod.controller import controller
from mod.tf.taba_factory import TabaFactory
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.ol.others_basic_action import others_basic_action_layer, obal_func
from mod.kihondousa import zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card
from mod.card import Card

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    else:
        huda.available_draw()

def _mousedown(huda: Huda) -> None:
    controller.active = huda
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def _active(huda: Huda) -> None:
    huda.detail_draw()
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        controller.data_transfer = huda
    else:
        source = {3: ACTION_CIRCLE_CARD, 2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
            int((diff_coord.angle_to([0, 0])+225)/90), ACTION_CIRCLE_ZENSIN)
        screen.blit(source=source, dest=controller.hold_coord-[250, 250])

# def _obal_func(cards: list[Card]=[], text: str="", mode: int=OBAL_KIHONDOUSA) -> Callable[[Huda], None]:
#     def func(huda: Huda) -> None:
#         if len(cards) == 1 and not cards[0].can_play(delivery=huda.delivery, hoyuusya=huda.hoyuusya, popup=True):
#             return
#         if text:
#             popup_message.add(text=text)
#         moderator.append(over_layer=others_basic_action_layer(
#             delivery=huda.delivery, hoyuusya=huda.hoyuusya, huda=huda, cards=cards, mode=mode))
#     return func

# _yadosi = _obal_func(cards=[yadosi_card])
# _basic = _obal_func(cards=[zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card], text="その他基本動作です")
# _zensin = _obal_func(cards=[zensin_card])
# _use_card: Callable[[Card], Callable[[Huda], None]] = lambda card: _obal_func(cards=[card], text=f"手札から「{card.name}」カードを使います", mode=OBAL_USE_CARD)

_yadosi = obal_func(cards=[yadosi_card])
_basic = obal_func(cards=[zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card], text="その他基本動作です")
_zensin = obal_func(cards=[zensin_card])
_use_card: Callable[[Card], Callable[[Huda], None]] = lambda card: obal_func(cards=[card], text=f"手札から「{card.name}」カードを使います", mode=OBAL_USE_CARD)

def _mouseup(huda: Huda) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50: return
    {3: _use_card(huda.card), 2: _yadosi, 1: _basic}.get(int((diff_coord.angle_to([0, 0])+225)/90), _zensin)(huda)

# def _use_card(huda: Huda) -> None:
#     if not huda.can_play(popup=True):
#         return
#     popup_message.add(text=f"手札から「{huda.card.name}」を使います")
#     huda.delivery.m_params(huda.hoyuusya).played_standard = True
#     huda.play()

def _drag(huda: Huda) -> None:
    gpv2 = Vector2(pygame.mouse.get_pos())
    pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.vertices], 20)
    huda.img_rz.set_alpha(192)
    screen.blit(source=huda.img_rz, dest=gpv2-Vector2(huda.img_rz.get_size())/2)
    huda.img_rz.set_alpha(255)

tehuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active, "mouseup": _mouseup, "drag": _drag
    }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
