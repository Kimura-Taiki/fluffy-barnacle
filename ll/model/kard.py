from pygame import Surface
from dataclasses import dataclass

from any.pictures import picload
from model.kard_core import KardCore

@dataclass(frozen=True)
class Kard():
    kard_core: KardCore
    png_file: str

    def picture(self) -> Surface:
        return picload(self.png_file)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Kard):
            return False
        return self.kard_core == other.kard_core
    
    @property
    def name(self) -> str:
        return self.kard_core.name
    
    @property
    def rank(self) -> int:
        return self.kard_core.rank
