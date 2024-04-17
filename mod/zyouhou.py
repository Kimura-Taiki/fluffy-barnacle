from pygame import Surface
from typing import Any

class Zyouhou():
    def __init__(self, siyousya: set[int], img: Surface, name: str, **kwargs: Any) -> None:
        self.siyousya = siyousya
        self.img = img
        self.name = name
        self.kwargs = kwargs