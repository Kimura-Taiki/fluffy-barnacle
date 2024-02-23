import pygame
from pygame.math import Vector2

from mod.classes import Youso, controller

def mousedown(youso: Youso) -> None:
    controller.active = youso
    controller.hold_coord = Vector2(pygame.mouse.get_pos())
