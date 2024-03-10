#                 20                  40                  60                 79
from pygame import Surface, Vector2
from pygame.locals import SRCALPHA

from mod.const import screen, BLACK, WHITE, MS_MINCHO_COL, FONT_SIZE_TATUZIN,\
    IMG_MAAI_AREA, IMG_DUST_AREA, draw_aiharasuu
from mod.mkt.utuwa import Utuwa

li: list[tuple[tuple[int, int], tuple[int, int, int]]] = [[(0, 2), WHITE],
    [(2, 0), WHITE], [(4, 2), WHITE], [(2, 4), WHITE], [(2, 2), BLACK]]

# def _img_text(text: str) -> Surface:
#     for i, (dest, color) in enumerate(li):
#         img_text = MS_MINCHO_COL(text, FONT_SIZE_TATUZIN, color)
#         if i == 0:
#             img_return = Surface(Vector2(img_text.get_size())+(4, 4), SRCALPHA)
#         img_return.blit(source=img_text, dest=dest)
#     return img_return

def _img_text(text: str) -> Surface:
    img_text = MS_MINCHO_COL(text, FONT_SIZE_TATUZIN, BLACK)
    img_siro = Surface(img_text.get_size(), SRCALPHA)
    img_siro.fill(color=WHITE)
    img_siro.set_alpha(192)
    img_return = Surface(img_text.get_size(), SRCALPHA)
    img_return.blit(source=img_siro, dest=(0, 0))
    img_return.blit(source=img_text, dest=(0, 0))
    return img_return

_MAAI_TEXT = _img_text("間合")
_TATUZIN_TEXT = _img_text("達人の間合い")
_DUST_TEXT = _img_text("ダスト")

def maai_draw(utuwa: Utuwa) -> None:
    screen.blit(source=utuwa.img, dest=-Vector2(utuwa.img.get_size())/2+[utuwa.x, utuwa.y])
    draw_aiharasuu(surface=screen, dest=-Vector2(utuwa.img.get_size())/2+(utuwa.x, utuwa.y), num=utuwa.delivery.b_params.maai)
    if utuwa.osame == utuwa.delivery.b_params.maai:
        screen.blit(source=_MAAI_TEXT, dest=utuwa.dest-_MAAI_TEXT.get_size()+(-30, 20))
    else:
        screen.blit(source=_img_text(f"間合({utuwa.osame})"), dest=utuwa.dest-_MAAI_TEXT.get_size()+(-80, 20))

def tatuzin_draw(dest: tuple[int, int], value: int) -> None:
    screen.blit(source=_TATUZIN_TEXT, dest=dest)
    draw_aiharasuu(surface=screen, dest=Vector2(dest)+(_TATUZIN_TEXT.get_width()-15, -15), num=value)

def dust_draw(utuwa: Utuwa) -> None:
    utuwa._draw()
    screen.blit(source=_DUST_TEXT, dest=utuwa.dest-_DUST_TEXT.get_size()+(-30, 20))
