from copy import deepcopy
from random import shuffle

from model.kard import Kard

_kard0 = Kard(name="(番兵)", rank=0, png_file="")
_kard1 = Kard(name="兵士", rank=1, png_file="img1")
_kard2 = Kard(name="道化", rank=2, png_file="img2")
_kard3 = Kard(name="騎士", rank=3, png_file="img3")
_kard4 = Kard(name="僧侶", rank=4, png_file="img4")
_kard5 = Kard(name="魔術師", rank=5, png_file="img5")
_kard6 = Kard(name="将軍", rank=6, png_file="img6")
_kard7 = Kard(name="大臣", rank=7, png_file="img7")
_kard8 = Kard(name="姫", rank=8, png_file="img8")
_kards = [_kard0, _kard1, _kard2, _kard3, _kard4, _kard5, _kard6, _kard7, _kard8]
_ids = [1]*5+[2, 3, 4, 5]*2+[6, 7, 8]

def make_deck() -> list[Kard]:
    deck = [deepcopy(_kards[i]) for i in _ids]
    shuffle(deck)
    return deck
