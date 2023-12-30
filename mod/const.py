import pygame
from pygame.surface import Surface
from typing import Callable

WX, WY = 1280, 720
FRAMES_PER_SECOND = 30
CARDS = 6
DHX = 120
DA = -6.0
HAND_ANGLE = lambda i: -DA/2*(CARDS-1)+DA*i
HAND_X = lambda i: WX/2-DHX/2*(CARDS-1)+DHX*i
HAND_Y = lambda i: WY-60+abs(i*2-(CARDS-1))**2*2
AIHARA_KURO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (0, 0, 0))
UTURO: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_n_{i}.png").convert_alpha()
