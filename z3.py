from dataclasses import dataclass
from typing import Callable

class Hoge():
    def __init__(self, band: int=0, text: str="", action: Callable[..., None] | None=None) -> None:
        self.band = band
        self.text = text
        if action:
            self.action = action
        else:
            self.action = PrintHoge(self).action

@dataclass
class PrintHoge():
    hoge: Hoge

    def action(self) -> None:
        band = "-"*self.hoge.band
        print(band+self.hoge.text+band)

hhh = Hoge(5, "huhuhu")
PrintHoge(hhh).action()
hhh.action()
