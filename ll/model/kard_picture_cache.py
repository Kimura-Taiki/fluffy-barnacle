from pygame import Surface, transform, Vector2 as V2, Rect
from dataclasses import dataclass, field

from any.font import LL_RENDER
from any.func import translucented_color, rect_fill
from any.locales import kames
from any.pictures import picload
from model.kard_core import KardCore

_load_count = 0
_create_count = 0
_TITLE = 54
_FONT = 18

@dataclass
class KardPictureCache:
    cache: dict[tuple[KardCore, str], Surface] = field(default_factory=dict)  # 修正: デフォルトは空の辞書

    def picture(self, key: tuple[KardCore, str]) -> Surface:
        if key in self.cache:
            global _load_count
            _load_count += 1
            # print("load_count=", _load_count)
            return self.cache[key]
        else:
            global _create_count
            _create_count += 1
            # print("create_count=", _create_count)
            new_surface = self._img(key=key)
            self.cache[key] = new_surface
            return new_surface

    def _img(self, key: tuple[KardCore, str]) -> Surface:
        kc, png_file = key
        img = picload(png_file)
        self._add_name(img=img, kc=kc)
        self._add_text(img=img, kc=kc)
        return img

    def _add_name(self, img: Surface, kc: KardCore) -> None:
        name = kc.name
        render = LL_RENDER(name(), _TITLE, "black")
        source = transform.rotozoom(surface=render, angle=0.0, scale=min(1.0, 190/render.get_width()))
        img.blit(source=source, dest=V2(220, 55)-V2(source.get_size())/2)

    def _add_text(self, img: Surface, kc: KardCore) -> None:
        li = self._text_list(kc=kc)
        margin = (100-len(li)*_FONT)/len(li)
        h = 355+margin/2
        for str in li:
            render = LL_RENDER(str, _FONT, "black")
            rv2 = V2(render.get_size())
            dv2 = (170-rv2.x/2, h)
            rect_fill(color=translucented_color("white"), rect=Rect(dv2, rv2), surface=img)
            img.blit(source=render, dest=dv2)
            h += margin+_FONT

    def _text_list(self, kc: KardCore) -> list[str]:
        folder = kc.id.to_yaml_key
        text = kames(folder=folder, key="text")
        li = text.split("\n")
        if li[-1] == "":
            li.pop()
        return li

kp_cache = KardPictureCache()