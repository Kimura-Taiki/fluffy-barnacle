from typing import Any

from mod.zyouhou import Zyouhou

class Card():
    def __init__(self, zh: Zyouhou, hoyuusya: int, ryouiki: set[int], **kwargs: Any) -> None:
        self.zh = zh
        self.hoyuusya = hoyuusya
        self.ryouiki = ryouiki
        self.kwargs = kwargs