import pygame
from pygame.locals import FULLSCREEN
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any, Protocol

def pass_func(any: Any=None) -> None:
    pass

def nie(text: str) -> Callable[[], None]:
    def raise_func() -> None:
        raise NotImplementedError(f"{text} が未注入です")
    return raise_func

def compatible_with(obj: Any, protocol: type) -> None:
    if not isinstance(obj, protocol):
        cls = obj if type(obj) == type else type(obj)
        raise NotImplementedError(f"{cls.__name__}は{protocol.__name__}規約を満たしていません")

def joined_commands(commands: list[Callable[[], None]]) -> Callable[[], None]:
    def mono_command() -> None:
        for command in commands:
            command()
    return mono_command

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
UTURO_S: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_s_{i}.png").convert_alpha()
HONOKA: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_b_n_{i}.png").convert_alpha()
HONOKA_S: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_b_s_{i}.png").convert_alpha()

ACTION_CIRCLE_NEUTRAL = pygame.image.load("pictures/action_circle_neutral.png").convert_alpha()
ACTION_CIRCLE_CARD = pygame.image.load("pictures/action_circle_card.png").convert_alpha()
ACTION_CIRCLE_BASIC = pygame.image.load("pictures/action_circle_basic.png").convert_alpha()
ACTION_CIRCLE_ZENSIN = pygame.image.load("pictures/action_circle_zensin.png").convert_alpha()
ACTION_CIRCLE_YADOSI = pygame.image.load("pictures/action_circle_yadosi.png").convert_alpha()
IMG_AURA_AREA = pygame.image.load("pictures/ouka_aura.png").convert_alpha()
IMG_FLAIR_AREA = pygame.image.load("pictures/ouka_flare.png").convert_alpha()
IMG_LIFE_AREA = pygame.image.load("pictures/ouka_life.png").convert_alpha()
IMG_SYUUTYUU_AREA = pygame.image.load("pictures/syuutyuu.png").convert_alpha()
IMG_MAAI_AREA = pygame.image.load("pictures/ouka_distance.png").convert_alpha()
IMG_DUST_AREA = pygame.image.load("pictures/ouka_shadow.png").convert_alpha()
IMG_GOTTENON_BG = pygame.image.load("pictures/gottenon.png").convert_alpha()
IMG_YAMAHUDA = pygame.transform.rotozoom(surface=pygame.image.load("pictures/back_340x475.png"), angle=4.0, scale=0.6).convert_alpha()
IMG_BACK = pygame.transform.rotozoom(surface=pygame.image.load("pictures/back_340x475.png"), angle=90.0, scale=0.6).convert_alpha()
IMG_YATUBA_BG = pygame.image.load("pictures/yatuha_bg.png").convert_alpha()
IMG_AIHARASUU = pygame.image.load("pictures/aiharasuu.png").convert_alpha()
def draw_aiharasuu(surface: Surface, dest: Vector2, num: int) -> None:
    surface.blit(source=IMG_AIHARASUU, dest=dest, area=[num%10*60, num//10*60, 60, 60])

HANTE = 0
SIMOTE = 1
KAMITE = 2

TC_INVALID = 0
TC_YAMAHUDA = 1
TC_TEHUDA = 2
TC_SUTEHUDA = 3
TC_HUSEHUDA = 4
TC_KIRIHUDA = 5
TC_MISIYOU = 6
TC_ZYOGAI = 7

UC_ZYOGAI = 7
UC_MAAI = 8
UC_DUST = 9
UC_AURA = 10
UC_FLAIR = 11
UC_LIFE = 12