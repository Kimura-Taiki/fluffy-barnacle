from pygame.surface import Surface
from pygame.locals import SRCALPHA
from pygame.math import Vector2
import pygame

from mod.const import IMG_OSAME, draw_aiharasuu, USAGE_DEPLOYED
from mod.huda import Huda

def draw_huyo(huda: Huda) -> None:
    if huda.usage != USAGE_DEPLOYED:
        huda.rearrange(angle=huda.angle, x=huda.x, y=huda.y)
        return
    img_osame = Surface(huda.img_nega.get_size(), flags=SRCALPHA)
    img_osame.blit(source=IMG_OSAME, dest=[0, 0])
    draw_aiharasuu(surface=img_osame, dest=Vector2(5, 0), num=huda.osame)
    img_rz_osame = pygame.transform.rotozoom(surface=img_osame, angle=huda.angle, scale=huda.scale)
    huda.img_rz.blit(source=img_rz_osame, dest=[0, 0])
