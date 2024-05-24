from typing import NamedTuple

class Kard(NamedTuple):
    name: str
    png_file: str

EMPTY_KARD = Kard(name="empty", png_file="")