#                 20                  40                  60                 79
from pygame.surface import Surface
from typing import Any

from mod.const import IMG_HAKUSI, MS_MINCHO_COL, BLACK, IMG_FT_ARROW, IMG_FT_OUKA, FONT_SIZE_CARD_TITLE\
    , IMG_FT_MAAI, IMG_FT_DUST, IMG_FT_ZYOGAI, IMG_FT_AI_AURA, IMG_FT_AI_FLAIR, IMG_FT_AI_LIFE, IMG_FT_AI_SYUUTYUU\
    , IMG_FT_ZI_AURA, IMG_FT_ZI_FLAIR, IMG_FT_ZI_LIFE, IMG_FT_ZI_SYUUTYUU, UC_MAAI, UC_DUST, UC_ZYOGAI\
    , UC_AURA, UC_FLAIR, UC_LIFE, UC_SYUUTYUU, CT_KOUDOU
from mod.classes import Delivery
from mod.card.card import Card, BoolDI, KoukaDI, auto_di, nega_di
from mod.card.kw.yazirusi import Yazirusi

__all__ = ['auto_di', 'nega_di']

class TempKoudou(Card):
    def __init__(self, name: str, cond: BoolDI, kouka: KoukaDI | None=None, todo: list[list[Any]]=[],
                 yazirusi: Yazirusi | list[Yazirusi]=[]) -> None:
        self.img = IMG_HAKUSI.copy()
        self.y = 20
        self._draw_name(name=name)
        if kouka:
            self._maid_by_kouka(name=name, cond=cond, kouka=kouka, todo=todo)
        elif yazirusi:
            self._maid_by_yazirusi(name=name, cond=cond, yazirusi=yazirusi)
        else:
            raise ValueError("koukaかyazirusiは必要だよ")

    def _maid_by_kouka(self, name: str, cond: BoolDI, kouka: KoukaDI, todo: list[list[Any]]=[]) -> None:
        for i in todo:
            if isinstance(i[0], bool):
                self._draw_yazirusi(from_mine=i[0], from_code=i[1], to_mine=i[2], to_code=i[3], kazu=i[4])
            elif isinstance(i[0], str):
                self._draw_text(texts=i)
        super().__init__(self.img, name, cond, CT_KOUDOU, kouka=kouka)

    def _maid_by_yazirusi(self, name: str, cond: BoolDI, yazirusi: Yazirusi | list[Yazirusi]) -> None:
        if isinstance(yazirusi, Yazirusi):
            li = [yazirusi]
        else:
            li = yazirusi
        for yazirusi in li:
            self._draw_yazirusi(from_mine=yazirusi.from_mine, from_code=yazirusi.from_code,
                to_mine=yazirusi.to_mine, to_code=yazirusi.to_code, kazu=yazirusi.kazu)
        def kouka(delivery: Delivery, hoyuusya: int) -> None:
            for yazirusi in li:
                yazirusi.send(delivery=delivery, hoyuusya=hoyuusya)
        super().__init__(self.img, name, cond, CT_KOUDOU, kouka=kouka)

    def _draw_name(self, name: str) -> None:
        for i, mozi in enumerate(name):
            self.img.blit(source=MS_MINCHO_COL(mozi, FONT_SIZE_CARD_TITLE, BLACK), dest=[0, i*FONT_SIZE_CARD_TITLE])

    def _draw_yazirusi(self, from_mine: bool, from_code: int, to_mine: bool, to_code: int, kazu: int) -> None:
        self.img.blit(source=self._img_target(is_mine=from_mine, utuwa_code=from_code), dest=[60, self.y])
        self.img.blit(source=self._img_target(is_mine=to_mine, utuwa_code=to_code), dest=[210, self.y])
        self.img.blit(source=IMG_FT_ARROW, dest=[130, self.y])
        for i in range(kazu):
            self.img.blit(source=IMG_FT_OUKA, dest=[140-kazu*5+i*10, self.y])
        self.y += 100

    def _img_target(self, is_mine: bool, utuwa_code: int) -> Surface:
        if not (target := (
            {UC_MAAI: IMG_FT_MAAI, UC_DUST: IMG_FT_DUST, UC_ZYOGAI: IMG_FT_ZYOGAI} |
            ({UC_AURA: IMG_FT_ZI_AURA, UC_FLAIR: IMG_FT_ZI_FLAIR, UC_LIFE: IMG_FT_ZI_LIFE, UC_SYUUTYUU: IMG_FT_ZI_SYUUTYUU}
             if is_mine else
             {UC_AURA: IMG_FT_AI_AURA, UC_FLAIR: IMG_FT_AI_FLAIR, UC_LIFE: IMG_FT_AI_LIFE,UC_SYUUTYUU: IMG_FT_AI_SYUUTYUU}))
             .get(utuwa_code)):
            raise ValueError(f"Invalid utuwa_code: {utuwa_code}")
        return target
    
    def _draw_text(self, texts: list[str]) -> None:
        self.y += 5
        for text in texts:
            self.img.blit(source=MS_MINCHO_COL(text, 20, BLACK), dest=[60, self.y])
            self.y += 20+2
        self.y += 5
