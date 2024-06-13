from pygame import Surface, Vector2 as V2, transform, Rect
from dataclasses import dataclass
from typing import Any

from any.font import LL_RENDER
from any.func import translucented_color, rect_fill
from any.locales import kames
from any.pictures import picload
from model.board import Board
from model.kard_core import KardCore
from model.player import Player
from ptc.bridge import Bridge

load_count = 0
_FONT = 18

@dataclass(frozen=True)
class InEffectKard():
    kard_core: KardCore
    png_file: str

    def picture(self) -> Surface:
        global load_count
        load_count += 1
        print("load_count=", load_count)
        return self._img()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InEffectKard):
            return False
        return self.kard_core == other.kard_core
    
    def _img(self) -> Surface:
        img = picload(self.png_file)
        self._add_name(img=img)
        self._add_text(img=img)
        return img

    def _add_name(self, img: Surface) -> None:
        name = self.kard_core.name
        render = LL_RENDER(name(), 54, "black")
        source = transform.rotozoom(surface=render, angle=0.0, scale=min(1.0, 190/render.get_width()))
        img.blit(source=source, dest=V2(220, 55)-V2(source.get_size())/2)

    def _add_text(self, img: Surface) -> None:
        li = self._text_list()
        margin = (100-len(li)*_FONT)/len(li)
        h = 355+margin/2
        for str in li:
            render = LL_RENDER(str, _FONT, "black")
            rv2 = V2(render.get_size())
            dv2 = (170-rv2.x/2, h)
            rect_fill(color=translucented_color("white"), rect=Rect(dv2, rv2), surface=img)
            img.blit(source=render, dest=dv2)
            h += margin+_FONT

    def _text_list(self) -> list[str]:
        folder = self.kard_core.id.to_yaml_key
        text = kames(folder=folder, key="text")
        li = text.split("\n")
        if li[-1] == "":
            li.pop()
        return li

    @property
    def name(self) -> str:
        return self.kard_core.name()
    
    @property
    def rank(self) -> int:
        return self.kard_core.rank
    
    def use_func(self, bridge: Bridge, player: Player) -> None:
        self.kard_core.use_func(bridge, player)