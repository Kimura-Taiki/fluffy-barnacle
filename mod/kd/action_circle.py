#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2

from mod.const import screen, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_YADOSI,\
    ACTION_CIRCLE_BASIC, ACTION_CIRCLE_ZENSIN, ACTION_CIRCLE_CARD, enforce,\
    OBAL_KIHONDOUSA, OBAL_SYUUTYUU, side_name
from mod.classes import Card, Youso, Huda, moderator, popup_message, controller
from mod.kd.kihondousa import zensin_card, ridatu_card, koutai_card,\
    matoi_card, yadosi_card
from mod.kd.hand_mono_kd_layer import hand_mono_kd_layer
from mod.kd.hand_kd_layer import hand_kd_layer
from mod.kd.syuutyuu_mono_kd_layer import syuutyuu_mono_kd_layer
from mod.kd.syuutyuu_kd_layer import syuutyuu_kd_layer
from mod.ol.use_hand_layer import use_hand_layer

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
        moderator.append(use_hand_layer(
            name=f"{side_name(youso.hoyuusya)}の「{cards[0].name}」を使います",
            card=cards[0], huda=enforce(youso, Huda)))
        return
    elif key == 2 and mode == OBAL_KIHONDOUSA:
        moderator.append(hand_mono_kd_layer(card=yadosi_card, huda=enforce(youso, Huda)))
        return
    elif key == 1 and mode == OBAL_KIHONDOUSA:
        moderator.append(hand_kd_layer(cards=
            [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card],
            huda=enforce(youso, Huda)))
        return
    elif (key == 4 or key == 0) and mode == OBAL_KIHONDOUSA:
        moderator.append(hand_mono_kd_layer(card=zensin_card, huda=enforce(youso, Huda)))
        return
    elif key == 3 and mode == OBAL_SYUUTYUU:
        popup_message.add("集中力はカードではありません")
        return
    elif key == 2 and mode == OBAL_SYUUTYUU:
        moderator.append(syuutyuu_mono_kd_layer(card=yadosi_card, delivery=youso.delivery, hoyuusya=youso.hoyuusya))
        return
    elif key == 1 and mode == OBAL_SYUUTYUU:
        moderator.append(syuutyuu_kd_layer(cards=
            [zensin_card, ridatu_card, koutai_card, matoi_card, yadosi_card],
            delivery=youso.delivery, hoyuusya=youso.hoyuusya))
        return
    elif (key == 4 or key == 0) and mode == OBAL_SYUUTYUU:
        moderator.append(syuutyuu_mono_kd_layer(card=zensin_card, delivery=youso.delivery, hoyuusya=youso.hoyuusya))
        return
    raise EOFError("ここに来たら問題だね")
