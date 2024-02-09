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
WHITE = (255, 255, 255)

FRAMES_PER_SECOND = 30
CARDS = 9
MS_MINCHO_COL: Callable[[str, int, tuple[int, int, int]], Surface] = lambda s, i, c: pygame.font.Font("msmincho001.ttf", i).render(s, True, c)
AIHARA_KURO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (0, 0, 0))
UTURO: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_n_{i}.png").convert_alpha()
UTURO_S: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_a_s_{i}.png").convert_alpha()
HONOKA: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_b_n_{i}.png").convert_alpha()
HONOKA_S: Callable[[int], Surface] = lambda i: pygame.image.load(f"cards/na_00_hajimari_b_s_{i}.png").convert_alpha()

FONT_SIZE_STACK_LOG = 24
FONT_SIZE_GOTTENON = 32
FONT_SIZE_POPUP_MESSAGE = 32
FONT_SIZE_TIMER = 32
FONT_SIZE_AIHARASUU = 60
FONT_SIZE_CARD_TITLE = 60

ACTION_CIRCLE_NEUTRAL = pygame.image.load("pictures/action_circle_neutral.png").convert_alpha()
ACTION_CIRCLE_CARD = pygame.image.load("pictures/action_circle_card.png").convert_alpha()
ACTION_CIRCLE_BASIC = pygame.image.load("pictures/action_circle_basic.png").convert_alpha()
ACTION_CIRCLE_ZENSIN = pygame.image.load("pictures/action_circle_zensin.png").convert_alpha()
ACTION_CIRCLE_YADOSI = pygame.image.load("pictures/action_circle_yadosi.png").convert_alpha()
KIRIHUDA_CIRCLE_NEUTRAL = pygame.image.load("pictures/kirihuda_circle_neutral.png").convert_alpha()
KIRIHUDA_CIRCLE_CARD = pygame.image.load("pictures/kirihuda_circle_card.png").convert_alpha()
IMG_USED = pygame.image.load("pictures/img_used.png").convert_alpha()
IMG_AURA_AREA = pygame.image.load("pictures/ouka_aura.png").convert_alpha()
IMG_FLAIR_AREA = pygame.image.load("pictures/ouka_flare.png").convert_alpha()
IMG_LIFE_AREA = pygame.image.load("pictures/ouka_life.png").convert_alpha()
IMG_ISYUKU_AREA = pygame.image.load("pictures/isyuku.png").convert_alpha()
IMG_SYUUTYUU_AREA = pygame.image.load("pictures/syuutyuu.png").convert_alpha()
IMG_MAAI_AREA = pygame.image.load("pictures/ouka_distance.png").convert_alpha()
IMG_DUST_AREA = pygame.image.load("pictures/ouka_shadow.png").convert_alpha()
IMG_ZYOGAI_AREA = pygame.image.load("pictures/ouka_excluded.png").convert_alpha()
IMG_GOTTENON_BG = pygame.image.load("pictures/gottenon.png").convert_alpha()
IMG_YAMAHUDA = pygame.transform.rotozoom(surface=pygame.image.load("pictures/back_340x475.png"), angle=4.0, scale=0.6).convert_alpha()
IMG_BACK = pygame.transform.rotozoom(surface=pygame.image.load("pictures/back_340x475.png"), angle=90.0, scale=0.6).convert_alpha()
IMG_YATUBA_BG = pygame.image.load("pictures/yatuha_bg.png").convert_alpha()
IMG_AIHARASUU = pygame.image.load("pictures/aiharasuu.png").convert_alpha()
_FSAS = FONT_SIZE_AIHARASUU
def draw_aiharasuu(surface: Surface, dest: Vector2, num: int, size: int=_FSAS) -> None:
    if size == _FSAS:
        surface.blit(source=IMG_AIHARASUU, dest=dest, area=[num%10*_FSAS, num//10*_FSAS, _FSAS, _FSAS])
    else:
        img_scale = Surface((_FSAS, _FSAS), pygame.SRCALPHA)
        img_scale.blit(source=IMG_AIHARASUU, dest=[0, 0], area=[num%10*_FSAS, num//10*_FSAS, _FSAS, _FSAS])
        surface.blit(source=pygame.transform.scale(img_scale, (size, size)), dest=dest)

IMG_GRAY_LAYER = pygame.image.load("pictures/gray_layer.png").convert_alpha()
IMG_AURA_DAMAGE = pygame.image.load("pictures/aura_damage.png").convert_alpha()
IMG_LIFE_DAMAGE = pygame.image.load("pictures/life_damage.png").convert_alpha()

IMG_HAKUSI = pygame.image.load("pictures/ft_hakusi.png").convert_alpha()
IMG_FT_MAAI = pygame.image.load("pictures/ft_maai.png").convert_alpha()
IMG_FT_DUST = pygame.image.load("pictures/ft_dust.png").convert_alpha()
IMG_FT_ZYOGAI = pygame.image.load("pictures/ft_zyogai.png").convert_alpha()
IMG_FT_ZI_AURA = pygame.image.load("pictures/ft_zi_aura.png").convert_alpha()
IMG_FT_ZI_FLAIR = pygame.image.load("pictures/ft_zi_flair.png").convert_alpha()
IMG_FT_ZI_LIFE = pygame.image.load("pictures/ft_zi_life.png").convert_alpha()
IMG_FT_ZI_SYUUTYUU = pygame.image.load("pictures/ft_zi_syuutyuu.png").convert_alpha()
IMG_FT_AI_AURA = pygame.image.load("pictures/ft_ai_aura.png").convert_alpha()
IMG_FT_AI_FLAIR = pygame.image.load("pictures/ft_ai_flair.png").convert_alpha()
IMG_FT_AI_LIFE = pygame.image.load("pictures/ft_ai_life.png").convert_alpha()
IMG_FT_AI_SYUUTYUU = pygame.image.load("pictures/ft_ai_syuutyuu.png").convert_alpha()
IMG_FT_ARROW = pygame.image.load("pictures/ft_arrow.png").convert_alpha()
IMG_FT_OUKA = pygame.image.load("pictures/ft_ouka.png").convert_alpha()

HANTE = 0
SIMOTE = 1
KAMITE = 2
opponent: Callable[[int], int] = lambda hoyuusya: KAMITE if hoyuusya == SIMOTE else SIMOTE if hoyuusya == KAMITE else hoyuusya
side_name: Callable[[int], str] = lambda hoyuusya: '下手' if hoyuusya == SIMOTE else '上手' if hoyuusya == KAMITE else '半手？'

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
UC_SYUUTYUU = 13
UC_ISYUKU = 14

MC_NONE = 0

CT_HUTEI = 0
CT_KOUGEKI = 1
CT_KOUDOU = 2
CT_HUYO = 3
CT_TAIOU = 4
CT_ZENRYOKU = 5

REQ_GET_HOVER = 1
REQ_OUKA = 2
REQ_TAIOU_TABA = 3

POP_TAIOUED = 101

USAGE_UNUSED = 0
USAGE_INUSE = 1
USAGE_DEPLOYED = 2
USAGE_USED = 3

PH_NONE = 0
PH_START = 1
PH_MAIN = 2
PH_END = 3