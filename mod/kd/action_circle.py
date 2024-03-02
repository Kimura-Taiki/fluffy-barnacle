#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2

from mod.const import screen, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_YADOSI,\
    ACTION_CIRCLE_BASIC, ACTION_CIRCLE_ZENSIN, ACTION_CIRCLE_CARD, enforce,\
    OBAL_KIHONDOUSA, OBAL_SYUUTYUU, OBAL_USE_CARD
from mod.classes import Callable, Card, Youso, Huda, Delivery, moderator, popup_message, controller
from mod.ol.others_basic_action import obal_func
from mod.kd.kihondousa import zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card
from mod.ol.standard_action_layer import use_card_layer

def mousedown(youso: Youso, mode: int=OBAL_KIHONDOUSA) -> None:
    if mode == OBAL_SYUUTYUU and youso.osame == 0:
        popup_message.add("集中力が0です")
        return
    controller.active = youso
    controller.hold_coord = Vector2(pygame.mouse.get_pos())

def active(youso: Youso, mode: int=OBAL_KIHONDOUSA) -> None:
    if mode == OBAL_KIHONDOUSA:
        enforce(youso, Huda).detail_draw()
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if (rr := diff_coord.length_squared()) < 50:
        screen.blit(source=ACTION_CIRCLE_NEUTRAL, dest=controller.hold_coord-[250, 250])
    elif rr > 62500:
        controller.active = None
    else:
        source = {3: ACTION_CIRCLE_CARD if mode == OBAL_KIHONDOUSA else ACTION_CIRCLE_NEUTRAL,
                  2: ACTION_CIRCLE_YADOSI, 1: ACTION_CIRCLE_BASIC}.get(
                      int((diff_coord.angle_to([0, 0])+225)/90), ACTION_CIRCLE_ZENSIN)
        screen.blit(source=source, dest=controller.hold_coord-[250, 250])

def mouseup(youso: Youso, mode: int=OBAL_KIHONDOUSA) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50: return
#                 20                  40                  60                 79
    cards: list[Card] = {
        3: [enforce(youso, Huda).card] if mode == OBAL_KIHONDOUSA else [],
        2: [yadosi_card],
        1: [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card]
        }.get(int((diff_coord.angle_to([0, 0])+225)/90),
           [zensin_card])
    if int((diff_coord.angle_to([0, 0])+225)/90) == 3 and mode == OBAL_KIHONDOUSA:
        mode = OBAL_USE_CARD
    moderator.append(use_card_layer(cards=cards, name="", youso=youso,
                                    mode=mode))

    # if int((diff_coord.angle_to([0, 0])+225)/90) == 3:
    #     moderator.append(use_card_layer(cards=[enforce(youso, Huda).card] if mode==OBAL_KIHONDOUSA else [],
    #                                     name="", youso=youso, mode=mode))
    # elif int((diff_coord.angle_to([0, 0])+225)/90) == 2:
    #     moderator.append(use_card_layer(cards=[yadosi_card], name="", youso=youso, mode=mode))
    # elif int((diff_coord.angle_to([0, 0])+225)/90) == 1:
    #     moderator.append(use_card_layer(cards=[zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card],
    #                                     name="", youso=youso, mode=mode))
    # else:
    #     moderator.append(use_card_layer(cards=[zensin_card], name="", youso=youso, mode=mode))

    # {3: _use_card(enforce(youso, Huda).card) if mode==OBAL_KIHONDOUSA else _not_card,
    #  2: obal_func(cards=[yadosi_card], name="標準行動：宿し", mode=mode),
    #  1: obal_func(cards=_available_basic_actions(youso.delivery, youso.hoyuusya), name="標準行動：その他基本動作", text="その他基本動作です", mode=mode)
    #  }.get(int((diff_coord.angle_to([0, 0])+225)/90),
    #        obal_func(cards=[zensin_card], name="標準行動：前進", mode=mode))(youso)

