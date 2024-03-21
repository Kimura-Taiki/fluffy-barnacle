#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2

from mod.const import screen, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_YADOSI,\
    ACTION_CIRCLE_BASIC, ACTION_CIRCLE_ZENSIN, ACTION_CIRCLE_CARD, enforce,\
    OBAL_KIHONDOUSA, OBAL_SYUUTYUU, OBAL_USE_CARD, side_name
from mod.classes import Card, Youso, Huda, moderator, popup_message, controller
from mod.kd.kihondousa import zensin_card, ridatu_card, koutai_card,\
    matoi_card, yadosi_card
from mod.ol.use_card_layer import use_card_layer

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
    key = int((diff_coord.angle_to([0, 0])+225)/90)
    cards: list[Card] = {
        3: [enforce(youso, Huda).card] if mode == OBAL_KIHONDOUSA else [],
        2: [yadosi_card],
        1: [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card]
        }.get(key,
           [zensin_card])
    if key == 3 and mode == OBAL_KIHONDOUSA:
        # mode = OBAL_USE_CARD
        print("uhl", f"{side_name(youso.hoyuusya)}の「{cards[0].name}」を使います", cards[0], enforce(youso, Huda))
        from mod.ol.use_hand_layer import use_hand_layer
        moderator.append(use_hand_layer(
            name=f"{side_name(youso.hoyuusya)}の「{cards[0].name}」を使います",
            card=cards[0], huda=enforce(youso, Huda)))
        return
    name = f"{side_name(youso.hoyuusya)}の「{cards[0].name}」を使います"\
        if mode == OBAL_USE_CARD else ""
    moderator.append(use_card_layer(cards=cards, name=name, youso=youso,
                                    mode=mode))
