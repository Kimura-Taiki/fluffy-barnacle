#                 20                  40                  60                 79
from pygame.math import Vector2
from typing import Any

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, TC_SUTEHUDA, side_name, POP_TAIOUED, POP_OK,\
    enforce, POP_AFTER_ATTACKED
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Card
from mod.taba import Taba
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.play_kougeki.uke_taba import uke_taba
from mod.ol.play_kougeki.taiou_taba import taiou_taba
from mod.ol.pop_stat import PopStat

SCALE_SIZE = 180

class PlayKougeki():
    def __init__(self, kougeki: Card, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int=POP_OK) -> None:
        self.kougeki = kougeki
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"攻撃:{kougeki.name}の使用"
        self.inject_func = delivery.inject_view
        self.taiou_taba: Taba = Taba()
        self.uke_taba: Taba = Taba()
        self.taiou_huda: Huda | None = None
        self.code = code

    def elapse(self) -> None:
        screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()
        self.taiou_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.uke_taba.get_hover_huda() or self.taiou_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        if not self.kougeki.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya, popup=True):
            moderator.pop()
            return
        self.uke_taba = uke_taba(kougeki=self.kougeki, discard_source=self._discard_source,
                                 delivery=self.delivery, hoyuusya=self.hoyuusya)
        self.taiou_taba = taiou_taba(delivery=self.delivery, hoyuusya=self.hoyuusya, kougeki=self.kougeki)

    def close(self) -> PopStat:
        self.kougeki.close(hoyuusya=self.hoyuusya)
        return PopStat(code=self.code, huda=self.source_huda)

    def moderate(self, stat: PopStat) -> None:
        enforce({POP_TAIOUED: self._taioued,
                 POP_AFTER_ATTACKED: self._after_attacked}.get(stat.code), type(self._taioued))(stat)
        
    def _taioued(self, stat: PopStat) -> None:
        if not isinstance(stat.huda, Huda):
            raise ValueError(f"Invalid stat: {stat}")
        self.taiou_huda = stat.huda
        self.taiou_taba.clear()
        if not self.kougeki.maai_cond(delivery=self.delivery, hoyuusya=self.hoyuusya):
            popup_message.add(text=f"{side_name(self.hoyuusya)}の「{self.kougeki.name}」が適正距離から外れました")
            self._discard_source()
            return
        self.kougeki = self.taiou_huda.card.taiounize(self.kougeki, self.delivery, self.hoyuusya)
        self.uke_taba = uke_taba(kougeki=self.kougeki, discard_source=self._discard_source,
                                 delivery=self.delivery, hoyuusya=self.hoyuusya)
        
    def _after_attacked(self, stat: PopStat) -> None:
        moderator.pop()

    def _discard_source(self) -> None:
        if self.source_huda:
            self.source_huda.discard()
        if self.kougeki.after:
            self.kougeki.after.kaiketu(
                delivery=self.delivery, hoyuusya=self.hoyuusya, huda=self.source_huda, code=POP_AFTER_ATTACKED)
            return
        moderator.pop()

# compatible_with(, OverLayer)
