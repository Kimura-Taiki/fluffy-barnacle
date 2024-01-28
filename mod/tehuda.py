#                 20                  40                  60                 79
import pygame
from pygame.math import Vector2
from typing import Callable

from mod.const import WX, WY, screen, BRIGHT, ACTION_CIRCLE_NEUTRAL, ACTION_CIRCLE_CARD, ACTION_CIRCLE_BASIC \
    , ACTION_CIRCLE_ZENSIN, ACTION_CIRCLE_YADOSI, TC_HUSEHUDA, UC_AURA, UC_FLAIR, UC_MAAI
from mod.huda import Huda, default_draw
from mod.controller import controller
from mod.taba_factory import TabaFactory
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.ol.others_basic_action import OthersBasicAction

HAND_X_RATE: Callable[[int], float] = lambda i: 120-130*max(0, i-4)/i
HAND_X: Callable[[int, int], int | float] = lambda i, j: WX/2-HAND_X_RATE(j)/2*(j-1)+HAND_X_RATE(j)*i

HAND_Y_DIFF: Callable[[int, int], float] = lambda i, j: abs(i*2-(j-1))*(1 if j < 3 else 3/(j-1))
HAND_Y: Callable[[int, int], int | float] = lambda i, j: WY-60+HAND_Y_DIFF(i, j)**2*2

HAND_ANGLE_RATE: Callable[[int], float] = lambda i: -6 if i < 3 else -6.0*3/(i-1)
HAND_ANGLE: Callable[[int, int], int | float] = lambda i, j: -HAND_ANGLE_RATE(j)/2*(j-1)+HAND_ANGLE_RATE(j)*i

def _draw(huda: Huda) -> None:
    if controller.active == huda:
        return None
    elif controller.hover == huda:
        pygame.draw.polygon(screen, BRIGHT, [i+[0, -40] for i in huda.vertices], 20)
        screen.blit(source=huda.img_rz, dest=huda.img_rz_topleft+[0, -40])
    else:
        default_draw(huda=huda)
    return None

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

def _mouseup(huda: Huda) -> None:
    diff_coord = pygame.mouse.get_pos()-controller.hold_coord
    if diff_coord.length_squared() < 50: return
    {3: _use_card, 2: _yadosi, 1: _basic}.get(int((diff_coord.angle_to([0, 0])+225)/90), _zensin)(huda=huda)

def _use_card(huda: Huda) -> None:
    popup_message.add(text="カードを使います")

def _yadosi(huda: Huda) -> None:
    if not huda.delivery.can_ouka_to_ryouiki(listener=huda, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR):
        popup_message.add(text="宿せません！")
        return
    popup_message.add(text="宿します")
    huda.delivery.send_ouka_to_ryouiki(listener=huda, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)
    huda.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

def _basic(huda: Huda) -> None:
    popup_message.add(text="その他基本動作です")
    moderator.append(over_layer=OthersBasicAction(inject_func=huda.delivery.inject_view))

def _zensin(huda: Huda) -> None:
    if not huda.delivery.can_ouka_to_ryouiki(listener=huda, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA):
        popup_message.add(text="前進できません！")
        return
    popup_message.add(text="前進します")
    huda.delivery.send_ouka_to_ryouiki(listener=huda, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)
    huda.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=TC_HUSEHUDA)

def _drag(huda: Huda) -> None:
    gpv2 = Vector2(pygame.mouse.get_pos())
    pygame.draw.polygon(screen, BRIGHT, [gpv2-huda.dest+i for i in huda.vertices], 20)
    huda.img_rz.set_alpha(192)
    screen.blit(source=huda.img_rz, dest=gpv2-Vector2(huda.img_rz.get_size())/2)
    huda.img_rz.set_alpha(255)

tehuda_factory = TabaFactory(inject_kwargs={
    "draw": _draw, "hover": Huda.detail_draw, "mousedown": _mousedown, "active": _active, "mouseup": _mouseup, "drag": _drag
    }, huda_x=HAND_X, huda_y=HAND_Y, huda_angle=HAND_ANGLE)
