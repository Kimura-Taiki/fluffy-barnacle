#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.locals import SRCALPHA
from pygame.math import Vector2

from mod.const import IMG_OSAME, draw_aiharasuu, USAGE_DEPLOYED, enforce,\
    TC_TEHUDA, TC_KIRIHUDA, IMG_ATTACK_STAT, CT_KOUGEKI, CT_HUYO, MS_MINCHO_COL, BLACK
from mod.classes import Huda, Taba

# def add_draw(huda: Huda) -> None:
#     {CT_KOUGEKI: draw_kougeki, CT_HUYO: draw_huyo}.get(
#         huda.card.type, draw_others)(huda)

# def draw_others(huda: Huda) -> None:
#     huda.img_detail = huda.img_nega.copy()


# def draw_kougeki(huda: Huda) -> None:
#     # tehuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), Taba)
#     # kirihuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA), Taba)
#     # if not huda in tehuda and not huda in kirihuda:
#     #     huda.rearrange(angle=huda.angle, x=huda.x, y=huda.y)
#     #     return
#     # img_stat = Surface(huda.img_nega.get_size(), flags=SRCALPHA)
#     img_stat = huda.img_nega.copy()
#     img_stat.blit(source=IMG_ATTACK_STAT, dest=[8, 385])
#     if huda.card.aura_bar(huda.delivery, huda.hoyuusya):
#         ...
#     else:
#         draw_aiharasuu(surface=img_stat, dest=Vector2(-2, 375), num=huda.card.aura_damage(huda.delivery, huda.hoyuusya))
#     if huda.card.life_bar(huda.delivery, huda.hoyuusya):
#         ...
#     else:
#         draw_aiharasuu(surface=img_stat, dest=Vector2(38, 405), num=huda.card.life_damage(huda.delivery, huda.hoyuusya))
#     huda.img_detail = img_stat

# def draw_huyo(huda: Huda) -> None:
#     if huda.usage != USAGE_DEPLOYED:
#         draw_others(huda=huda)
#         return
#     img_osame = huda.img_nega.copy()
#     img_osame.blit(source=IMG_OSAME, dest=[0, 0])
#     draw_aiharasuu(surface=img_osame, dest=Vector2(5, 0), num=huda.osame)
#     huda.img_detail = img_osame

def detail(huda: Huda) -> Surface:
    return {CT_KOUGEKI: _kougeki_detail, CT_HUYO: _huyo_detail}.get(
        huda.card.type, _others_detail)(huda)

def _others_detail(huda: Huda) -> Surface:
    return huda.img_nega.copy()

def _kougeki_detail(huda: Huda) -> Surface:
    # tehuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), Taba)
    # kirihuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA), Taba)
    # if not huda in tehuda and not huda in kirihuda:
    #     huda.rearrange(angle=huda.angle, x=huda.x, y=huda.y)
    #     return
    # img_stat = Surface(huda.img_nega.get_size(), flags=SRCALPHA)
    detail = huda.img_nega.copy()
    detail.blit(source=IMG_ATTACK_STAT, dest=[8, 385])
    if huda.card.aura_bar(huda.delivery, huda.hoyuusya):
        ...
    else:
        draw_aiharasuu(surface=detail, dest=Vector2(-2, 375), num=huda.card.aura_damage(huda.delivery, huda.hoyuusya))
    if huda.card.life_bar(huda.delivery, huda.hoyuusya):
        ...
    else:
        draw_aiharasuu(surface=detail, dest=Vector2(38, 405), num=huda.card.life_damage(huda.delivery, huda.hoyuusya))
    return detail

def _huyo_detail(huda: Huda) -> Surface:
    if huda.usage != USAGE_DEPLOYED:
        return _others_detail(huda=huda)
    detail = huda.img_nega.copy()
    detail.blit(source=IMG_OSAME, dest=[0, 0])
    draw_aiharasuu(surface=detail, dest=Vector2(5, 0), num=huda.osame)
    return detail
