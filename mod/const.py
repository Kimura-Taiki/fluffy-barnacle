import pygame
from pygame.locals import FULLSCREEN
from pygame.surface import Surface
from typing import Callable, Any, Protocol

def pass_func(any: Any=None) -> None:
    pass

def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(f"{text} が未注入です")
    return raise_func

def compatible_with(cls: type, protocol: type):
    if not isinstance(cls, protocol):
        raise NotImplementedError(f"{cls.__name__}は{protocol.__name__}規約を満たしていません")

WX, WY = 1280, 720
pygame.init()
pygame.display.set_caption("FFF")
screen = pygame.display.set_mode((WX, WY))
clock = pygame.time.Clock()

BRIGHT = (255, 255, 255, 128)
GAINSBORO = (220, 220, 220)
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

ACTION_CIRCLE_NEUTRAL = pygame.image.load("pictures/action_circle_neutral.png").convert_alpha()
ACTION_CIRCLE_CARD = pygame.image.load("pictures/action_circle_card.png").convert_alpha()
ACTION_CIRCLE_BASIC = pygame.image.load("pictures/action_circle_basic.png").convert_alpha()
IMG_AURA_AREA = pygame.image.load("pictures/ouka_aura.png").convert_alpha()
IMG_FLAIR_AREA = pygame.image.load("pictures/ouka_flare.png").convert_alpha()
IMG_LIFE_AREA = pygame.image.load("pictures/ouka_life.png").convert_alpha()
IMG_SYUUTYUU_AREA = pygame.image.load("pictures/syuutyuu.png").convert_alpha()
IMG_GOTTENON_BG = pygame.image.load("pictures/gottenon.png").convert_alpha()
IMG_BACK = pygame.transform.rotozoom(surface=pygame.image.load("pictures/back_340x475.png"), angle=90.0, scale=0.6).convert_alpha()

TC_YAMAHUDA = 1
TC_TEHUDA = 2
TC_SUTEHUDA = 3
TC_HUSEHUDA = 4
TC_KIRIHUDA = 5
TC_MISIYOU = 6
TC_ZYOGAI = 7