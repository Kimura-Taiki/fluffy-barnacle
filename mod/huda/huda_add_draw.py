#                 20                  40                  60                 79
import pygame
from pygame.surface import Surface
from pygame.math import Vector2

from mod.const import IMG_OSAME, draw_aiharasuu, USAGE_DEPLOYED, enforce,\
    TC_TEHUDA, TC_KIRIHUDA, IMG_ATTACK_STAT, CT_KOUGEKI, CT_HUYO,\
    MS_MINCHO_COL, BLACK, FONT_SIZE_MAAI, WHITE
from mod.classes import Huda, Taba
from mod.card.card_func import maai_text

def img_detail(huda: 'Huda') -> Surface:
    return {CT_KOUGEKI: _kougeki_detail, CT_HUYO: _huyo_detail}.get(
        huda.card.type, _others_detail)(huda)

def _others_detail(huda: 'Huda') -> Surface:
    return huda.huda_draw.img_nega.copy()

def _damage_detail(huda: 'Huda', img: Surface) -> Surface:
    img.blit(source=IMG_ATTACK_STAT, dest=[8, 385])
    if (ad := huda.card.aura_damage(delivery=huda.delivery, hoyuusya=huda.hoyuusya)) is not None:
        draw_aiharasuu(surface=img, dest=Vector2(-2, 375), num=ad)
    if (ld := huda.card.life_damage(delivery=huda.delivery, hoyuusya=huda.hoyuusya)) is not None:
        draw_aiharasuu(surface=img, dest=Vector2(38, 405), num=ld)
    return img

def _maai_detail(huda: 'Huda', img: Surface) -> Surface:
    text = MS_MINCHO_COL(maai_text(huda.card.maai_list(huda.delivery, huda.hoyuusya)), FONT_SIZE_MAAI, BLACK)
    pygame.draw.rect(img, WHITE, (45, 7, text.get_width(), text.get_height()), width=0)
    img.blit(source=text, dest=[45, 7])
    return img

def _kougeki_detail(huda: 'Huda') -> Surface:
    if huda.delivery.is_duck():
        return _others_detail(huda=huda)
    tehuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), Taba)
    kirihuda = enforce(huda.delivery.taba_target(hoyuusya=huda.hoyuusya, is_mine=True, taba_code=TC_KIRIHUDA), Taba)
    if not huda in tehuda and not huda in kirihuda:
        return _others_detail(huda=huda)
    detail = huda.huda_draw.img_nega.copy()
    detail = _damage_detail(huda=huda, img=detail)
    detail = _maai_detail(huda=huda, img=detail)
    # detail.blit(source=IMG_ATTACK_STAT, dest=[8, 385])
    # if (ad := huda.card.aura_damage(delivery=huda.delivery, hoyuusya=huda.hoyuusya)) is not None:
    #     draw_aiharasuu(surface=detail, dest=Vector2(-2, 375), num=ad)
    # if (ld := huda.card.life_damage(delivery=huda.delivery, hoyuusya=huda.hoyuusya)) is not None:
    #     draw_aiharasuu(surface=detail, dest=Vector2(38, 405), num=ld)
    return detail

def _huyo_detail(huda: 'Huda') -> Surface:
    if huda.usage != USAGE_DEPLOYED:
        return _others_detail(huda=huda)
    detail = huda.huda_draw.img_nega.copy()
    detail.blit(source=IMG_OSAME, dest=[0, 0])
    draw_aiharasuu(surface=detail, dest=Vector2(5, 0), num=huda.osame)
    return detail
