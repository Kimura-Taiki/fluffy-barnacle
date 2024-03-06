from typing import Any
from functools import partial

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, POP_VIEWED_BANMEN
from mod.delivery import Delivery, duck_delivery
from mod.ol.undo_mouse import make_undo_youso
from mod.ol.over_layer import OverLayer
from mod.huda.huda import Huda
from mod.popup_message import popup_message
from mod.controller import controller
from mod.moderator import moderator
from mod.youso import Youso
from mod.req.req_get_hover import ReqGetHover
from mod.ol.pop_stat import PopStat

_undo_youso = make_undo_youso(text="PlayKougeki")

class ViewBanmen():
    def __init__(self, delivery: Delivery) -> None:
        self.name = "盤面の確認中"
        self.inject_func = delivery.inject_view
        self.delivery = delivery
        self.hoyuusya = -1

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return self.delivery.respond(request=ReqGetHover()) or _undo_youso

    def open(self) -> None:
        ...

    def close(self) -> PopStat:
        return PopStat(POP_VIEWED_BANMEN)

    def moderate(self, stat: PopStat) -> None:
        ...

compatible_with(ViewBanmen(delivery=duck_delivery), OverLayer)

def _view_mouseup(huda: Huda) -> None:
    # popup_message.add(text=f"ViewBanmen's_undo.mouseup でクリック確定したよ")
    moderator.append(over_layer=ViewBanmen(delivery=huda.delivery))

view_youso = Youso(mousedown=Huda.mousedown, mouseup=_view_mouseup)