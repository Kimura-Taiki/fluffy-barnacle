#                 20                  40                  60                 79
from mod.const import CF_ATTACK_CORRECTION
from mod.card import TaiounizeDI

class Continuous():
    def __init__(self, type: int=0, taiounize: TaiounizeDI | None=None) -> None:
        self.type = type
        self.taiounize = taiounize