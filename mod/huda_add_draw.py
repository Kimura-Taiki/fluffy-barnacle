#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.locals import SRCALPHA
from pygame.math import Vector2

from mod.const import IMG_OSAME, draw_aiharasuu, USAGE_DEPLOYED, enforce,\
    TC_TEHUDA, TC_KIRIHUDA, IMG_ATTACK_STAT, CT_KOUGEKI, CT_HUYO
from mod.classes import Huda, Taba

def add_draw(huda: Huda) -> None:
    {CT_KOUGEKI: draw_kougeki, CT_HUYO: draw_huyo}.get(
        huda.card.type,Huda.default_draw)(huda)

def draw_kougeki(huda: Huda) -> None:
    tehuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), Taba)
    kirihuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA), Taba)
    if not huda in tehuda and not huda in kirihuda:
        huda.rearrange(angle=huda.angle, x=huda.x, y=huda.y)
        return
    img_stat = Surface(huda.img_nega.get_size(), flags=SRCALPHA)
    img_stat.blit(source=IMG_ATTACK_STAT, dest=[8, 385])
    img_rz_stat = pygame.transform.rotozoom(surface=img_stat, angle=huda.angle, scale=huda.scale)
    huda.img_rz.blit(source=img_rz_stat, dest=[0, 0])

def draw_huyo(huda: Huda) -> None:
    if huda.usage != USAGE_DEPLOYED:
        huda.rearrange(angle=huda.angle, x=huda.x, y=huda.y)
        return
    img_osame = Surface(huda.img_nega.get_size(), flags=SRCALPHA)
    img_osame.blit(source=IMG_OSAME, dest=[0, 0])
    draw_aiharasuu(surface=img_osame, dest=Vector2(5, 0), num=huda.osame)
    img_rz_osame = pygame.transform.rotozoom(surface=img_osame, angle=huda.angle, scale=huda.scale)
    huda.img_rz.blit(source=img_rz_osame, dest=[0, 0])