from pygame import Surface
from dataclasses import dataclass

from any.pictures import picload

@dataclass(frozen=True)
class Kard():
    name: str
    rank: int
    png_file: str

    def picture(self) -> Surface:
        return picload(self.png_file)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Kard):
            return False
        return self.name == other.name and self.rank == other.rank
