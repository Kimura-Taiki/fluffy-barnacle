import pygame
from pygame.locals import FULLSCREEN
from pygame.surface import Surface
from typing import Callable, Any

def pass_func(any: Any=None) -> None:
    pass

WX, WY = 1280, 720
pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

BRIGHT = (255, 255, 255, 128)
LEMONCHIFFON = (255, 250, 205)
BLACK = (0, 0, 0)

FRAMES_PER_SECOND = 30
CARDS = 9
_MS_MINCHO_32PT_FONT = pygame.font.Font("msmincho001.ttf", 32)
MS_MINCHO_32PT: Callable[[str], Surface] = lambda s: _MS_MINCHO_32PT_FONT.render(s, True, (0, 0, 0))
AIHARA_KURO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (0, 0, 0))
MS_MINCHO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("msmincho001.ttf", i).render(s, True, (0, 0, 0))
UTURO: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_n_{i}.png").convert_alpha()
HONOKA: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_b_n_{i}.png").convert_alpha()

ACTION_CIRCLE_NEUTRAL = pygame.image.load("pictures/action_circle_neutral.png")
ACTION_CIRCLE_CARD = pygame.image.load("pictures/action_circle_card.png")
ACTION_CIRCLE_BASIC = pygame.image.load("pictures/action_circle_basic.png")
