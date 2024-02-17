#                 20                  40                  60                 79
from typing import Any

from mod.const import WX, WY, POP_TAIOUED
from mod.huda import Huda
from mod.moderator import moderator
from mod.ol.pop_stat import PopStat
from mod.ol.kaiketu_layer_facotry import kaiketu_layer_factory
from mod.delivery import Delivery

def _dih(delivery: Delivery, hoyuusya: int, huda: Huda) -> None:
    huda.card.kaiketu(delivery, hoyuusya, huda=huda)

PlayTaiou = kaiketu_layer_factory(name="の対応時効果", code=POP_TAIOUED, dih=_dih)
