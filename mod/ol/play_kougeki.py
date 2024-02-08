#                 20                  40                  60                 79
from pygame.math import Vector2
from typing import Any, Callable

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, TC_SUTEHUDA, POP_TAIOUED, side_name
from mod.huda import Huda
from mod.ol.view_banmen import view_youso
from mod.card import Kougeki
from mod.taba import Taba
from mod.tf.taba_factory import TabaFactory
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.delivery import Delivery
from mod.ol.play_taiou import PlayTaiou
from mod.ol.uke_taba import make_uke_taba
from mod.ol.taiou_taba import make_taiou_taba

HAND_ANGLE: Callable[[int, int], float] = lambda i, j: 0.0
HAND_UX: Callable[[int, int], float] = lambda i, j: WX/2-100*(j-1)+200*i
HAND_UY: Callable[[int, int], float] = lambda i, j: WY-150
SCALE_SIZE = 180

class PlayKougeki():
    def __init__(self, kougeki: Kougeki, delivery: Delivery, hoyuusya: int, huda: Any | None) -> None:
        self.kougeki = kougeki
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.source_huda = huda if isinstance(huda, Huda) else None
        self.name = f"攻撃:{kougeki.name}の使用"
        self.inject_func = delivery.inject_view
        self.taiou_taba: Taba = Taba()
        self.origin_list: list[Huda] = []
        self.uke_taba: Taba = Taba()
        self.taiou_factory = TabaFactory(inject_kwargs={
            "draw": Huda.available_draw, "hover": Huda.detail_draw, "mousedown": Huda.mousedown, "mouseup": self._taiou_mouseup
            }, huda_x=HAND_UX, huda_y=HAND_UY, huda_angle=HAND_ANGLE)
        self.taiou_huda: Huda | None = None

    def elapse(self) -> None:
        screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
        screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
        self.uke_taba.elapse()
        self.taiou_taba.elapse()

    def get_hover(self) -> Any | None:
        return self.uke_taba.get_hover_huda() or self.taiou_taba.get_hover_huda() or view_youso

    def open(self) -> None:
        self.uke_taba = make_uke_taba(kougeki=self.kougeki, discard_source=self._discard_source,
                                      delivery=self.delivery, hoyuusya=self.hoyuusya)
        # self._make_taiou_taba()
        self.taiou_taba = make_taiou_taba(delivery=self.delivery, hoyuusya=self.hoyuusya)

    def close(self) -> int:
        self.kougeki.close(hoyuusya=self.hoyuusya)
        return 0

    def moderate(self, stat: Any) -> None:
        print("moderate")
        # if stat != POP_TAIOUED or not self.taiou_huda:
        #     return
        if not isinstance(stat, tuple) or not isinstance(stat[1], Huda):
            return
        self.taiou_huda = stat[1]
        print("taioued")
        self.taiou_taba.clear()
        if not self.kougeki.maai_cond(delivery=self.delivery, hoyuusya=self.hoyuusya):
            popup_message.add(text=f"{side_name(self.hoyuusya)}の「{self.kougeki.name}」が適正距離から外れました")
            self._discard_source()
            return
        print(self.taiou_huda.card.name)
        self.kougeki = self.taiou_huda.card.taiounize(self.kougeki, self.delivery, self.hoyuusya)
        self.uke_taba = make_uke_taba(kougeki=self.kougeki, discard_source=self._discard_source,
                                      delivery=self.delivery, hoyuusya=self.hoyuusya)

    def _discard_source(self) -> None:
        if self.source_huda:
            self.delivery.send_huda_to_ryouiki(huda=self.source_huda, is_mine=True, taba_code=TC_SUTEHUDA)
        moderator.pop()

    def _taiou_mouseup(self, huda: Huda) -> None:
        if (number := next((i for i, v in enumerate(self.taiou_taba) if v == huda))) is None:
            raise ValueError(f"Invalid huda: {huda}")
        self.taiou_huda = self.origin_list[number]
        moderator.append(over_layer=PlayTaiou(huda=self.taiou_huda))

    def _make_taiou_taba(self) -> None:
        from mod.const import TC_TEHUDA
        if not isinstance(tehuda := self.delivery.taba_target(hoyuusya=self.hoyuusya, is_mine=False, taba_code=TC_TEHUDA), Taba):
            raise ValueError(f"Invalid tehuda: {tehuda}")
        self.origin_list = [huda for huda in tehuda if huda.card.taiou]
        self.taiou_taba = self.taiou_factory.maid_by_cards(cards=[huda.card for huda in self.origin_list], hoyuusya=self.hoyuusya)

# compatible_with(, OverLayer)
