#                 20                  40                  60                 79
from pygame import Surface, Vector2
from pygame.locals import SRCALPHA

from mod.const import BLACK, WHITE, MS_MINCHO_COL, FONT_SIZE_TATUZIN,\
    IMG_MAAI_AREA, IMG_DUST_AREA

li: list[tuple[tuple[int, int], tuple[int, int, int]]] = [[(0, 2), WHITE],
    [(2, 0), WHITE], [(4, 2), WHITE], [(2, 4), WHITE], [(2, 2), BLACK]]

def _img_text(text: str) -> Surface:
    for i, (dest, color) in enumerate(li):
        img_text = MS_MINCHO_COL(text, FONT_SIZE_TATUZIN, color)
        if i == 0:
            img_return = Surface(Vector2(img_text.get_size())+(4, 4), SRCALPHA)
        img_return.blit(source=img_text, dest=dest)
    return img_return

_MAAI_TEXT = _img_text("間合")
_TATUZIN_TEXT = _img_text("達人の間合い")
_DUST_TEXT = _img_text("ダスト")

def maai_draw(dest: tuple[int, int], value: int) -> None:
    

def tatuzin_draw(dest: tuple[int, int], value: int) -> None:
    ...

def dust_draw(dest: tuple[int, int], value: int) -> None:
    ...