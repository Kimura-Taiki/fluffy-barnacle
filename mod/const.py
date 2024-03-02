import pygame
from pygame.locals import FULLSCREEN
from pygame.surface import Surface
from pygame.math import Vector2
from typing import Callable, Any, TypeVar
from inspect import signature

T = TypeVar('T')

def enforce(__object: Any, __type: type[T]) -> T:
    if not isinstance(__object, __type):
        raise ValueError(f"{__object} is not an instance of {__type.__name__}")
    return __object

def print_signature(title: str, obj: Any) -> None:
    print(title)
    # 引数情報を取得
    args = signature(obj).parameters.values()
    for arg in args:
        print(f"Parameter {arg.name} Type: {arg.annotation}")
    # 戻り値の情報を取得
    return_type = signature(obj).return_annotation
    print(f"Return Type: {return_type}")

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
FONT_SIZE_OSAME_NUM = 120
FONT_SIZE_TITLE = 48

ACTION_CIRCLE_NEUTRAL = pygame.image.load("pictures/action_circle_neutral.png").convert_alpha()
ACTION_CIRCLE_CARD = pygame.image.load("pictures/action_circle_card.png").convert_alpha()
ACTION_CIRCLE_BASIC = pygame.image.load("pictures/action_circle_basic.png").convert_alpha()
ACTION_CIRCLE_ZENSIN = pygame.image.load("pictures/action_circle_zensin.png").convert_alpha()
ACTION_CIRCLE_YADOSI = pygame.image.load("pictures/action_circle_yadosi.png").convert_alpha()
KIRIHUDA_CIRCLE_NEUTRAL = pygame.image.load("pictures/kirihuda_circle_neutral.png").convert_alpha()
KIRIHUDA_CIRCLE_CARD = pygame.image.load("pictures/kirihuda_circle_card.png").convert_alpha()

IMG_DECISION = pygame.image.load("pictures/decision.png").convert_alpha()
IMG_DECISION_LIGHTEN = pygame.image.load("pictures/decision_lighten.png").convert_alpha()
IMG_TURN_END = pygame.image.load("pictures/turn_end.png").convert_alpha()
IMG_TURN_END_LIGHTEN = pygame.image.load("pictures/turn_end_lighten.png").convert_alpha()
IMG_OSAME_DUST = pygame.image.load("pictures/osame_dust.png").convert_alpha()
IMG_OSAME_DUST_LIGHTEN = pygame.image.load("pictures/osame_dust_lighten.png").convert_alpha()
IMG_OSAME_AURA = pygame.image.load("pictures/osame_aura.png").convert_alpha()
IMG_OSAME_AURA_LIGHTEN = pygame.image.load("pictures/osame_aura_lighten.png").convert_alpha()

HUDA_SCALE = 0.6
IMG_ATTACK_STAT = pygame.image.load("pictures/attack_stat.png").convert_alpha()
IMG_OSAME = pygame.image.load("pictures/osame_frame.png").convert_alpha()
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

IMG_BOOL_ZE = pygame.image.load("pictures/bool_ze.png").convert_alpha()
IMG_BOOL_HI = pygame.image.load("pictures/bool_hi.png").convert_alpha()

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
UC_TATUZIN = 15

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

POP_OK = 0
POP_START_PHASE_FINISHED = 1
POP_MAIN_PHASE_FINISHED = 2
POP_END_PHASE_FINISHED = 3
POP_TAIOUED = 101
POP_RECEIVED = 102
POP_AFTER_ATTACKED = 103
POP_HUYO_ELAPSED = 201
POP_RESHUFFLE_SELECTED = 202
POP_RESHUFFLED = 203
POP_TURN_DRAWED = 204
POP_HAKIZI_DID = 301
POP_VIEWED_BANMEN = 401
POP_DAMAGED_1 = 501
POP_DAMAGED_2 = 502
POP_VALIDATED = 601
POP_CHOICED = 602
POP_KAIKETUED = 603
POP_PLAYED_STANDARD = 604
POP_END_TRIGGERED = 701
POP_DISCARDED = 702
POP_OPEN = 703
POP_SYOUSOU_SELECTED = 801
POP_SYOUSOU_DAMAGED = 802

USAGE_UNUSED = 0
USAGE_INUSE = 1
USAGE_DEPLOYED = 2
USAGE_USED = 3

PH_NONE = 0
PH_START = 1
PH_MAIN = 2
PH_END = 3

OBAL_KIHONDOUSA = 0
OBAL_SYUUTYUU = 1
OBAL_USE_CARD = 2

CF_ATTACK_CORRECTION = 1
CF_TRIGGER = 2

TG_1_OR_MORE_DAMAGE = 1
TG_2_OR_MORE_DAMAGE = 2
TG_END_PHASE = 3

DMG_DEFAULT = 0
DMG_RESHUFFLE = 1
DMG_SYOUSOU = 2

MG_YURINA = 1
MG_SAINE = 2
MG_HIMIKA = 3
MG_TOKOYO = 4
MG_OBORO = 5
MG_YUKIHI = 6
MG_SINRA = 7
MG_HAGANE = 8
MG_TIKAGE = 9
MG_KURURU = 10
MG_SARIYA = 11
MG_RAIRA = 12
MG_UTURO = 13
MG_HONOKA = 14
MG_KORUNU = 15
MG_YATUHA = 16
MG_HATUMI = 17
MG_MIZUKI = 18
MG_MEGUMI = 19
MG_KANAWE = 20
MG_KAMUWI = 21
MG_RENRI = 22
MG_AKINA = 23
MG_SISUI = 24
MG_MISORA = 25
