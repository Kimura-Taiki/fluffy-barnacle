from copy import deepcopy
from random import shuffle

from model.kard import Kard

_params: list[tuple[str, int, str]] = [
    ("兵士", 1, "img11a"), ("兵士", 1, "img11b"), ("兵士", 1, "img11c"), ("兵士", 1, "img11d"), 
    ("兵士", 1, "img11e"), ("道化", 2, "img12a"), ("道化", 2, "img12b"), ("騎士", 3, "img13a"), 
    ("騎士", 3, "img13b"), ("僧侶", 4, "img14a"), ("僧侶", 4, "img14b"), ("魔術師", 5, "img15a"), 
    ("魔術師", 5, "img15b"), ("将軍", 6, "img16a"), ("大臣", 7, "img17a"), ("姫", 8, "img18a"), 
]
_deck = [Kard(name=name, rank=rank, png_file=f"dere1/{png_file}") for name, rank, png_file in _params]

KARD_BANPEI = Kard(name="(番兵)", rank=0, png_file="")
KARD_HEISI = _deck[0]
KARD_DOUKE = _deck[5]
KARD_KISI = _deck[7]
KARD_SOURYO = _deck[9]
KARD_MAZYUTUSI = _deck[11]
KARD_SYOUGUN = _deck[13]
KARD_DAIZIN = _deck[14]
KARD_HIME = _deck[15]

_kards: list[Kard] = [
    KARD_BANPEI, KARD_HEISI, KARD_DOUKE, KARD_KISI, KARD_SOURYO, 
    KARD_MAZYUTUSI, KARD_SYOUGUN, KARD_DAIZIN, KARD_HIME
]

def make_deck() -> list[Kard]:
    deck = deepcopy(_deck)
    shuffle(deck)
    return deck

print("make_deck", make_deck())
print("_deck", _deck)

# KARD_BANPEI = Kard(name="(番兵)", rank=0, png_file="")
# KARD_HEISI = Kard(name="兵士", rank=1, png_file="img1")
# KARD_DOUKE = Kard(name="道化", rank=2, png_file="img2")
# KARD_KISI = Kard(name="騎士", rank=3, png_file="img3")
# KARD_SOURYO = Kard(name="僧侶", rank=4, png_file="img4")
# KARD_MAZYUTUSI = Kard(name="魔術師", rank=5, png_file="img5")
# KARD_SYOUGUN = Kard(name="将軍", rank=6, png_file="img6")
# KARD_DAIZIN = Kard(name="大臣", rank=7, png_file="img7")
# KARD_HIME = Kard(name="姫", rank=8, png_file="img8")
# _kards = [KARD_BANPEI, KARD_HEISI, KARD_DOUKE, KARD_KISI, KARD_SOURYO,
#           KARD_MAZYUTUSI, KARD_SYOUGUN, KARD_DAIZIN, KARD_HIME
# ]
# _ids = [1]*5+[2, 3, 4, 5]*2+[6, 7, 8]

# def make_deck() -> list[Kard]:
#     deck = [deepcopy(_kards[i]) for i in _ids]
#     shuffle(deck)

#     # # 「姫」の処理を実装する為に１枚目を姫に修正
#     # deck.insert(0, _kards[8])

#     # # 「大臣」の処理を実装する為に１枚目を大臣に修正
#     # deck.insert(0, _kards[7])
#     # deck.insert(1, _kards[7])
#     # deck.insert(4, _kards[8])
#     # deck.insert(5, _kards[1])

#     # # 「将軍」の処理を実装する為に１枚目を将軍に変更
#     # deck.insert(0, _kards[6])

#     # # 「魔術師」
#     # deck.insert(0, _kards[5])
#     # deck.insert(1, _kards[8])
#     # deck.insert(2, _kards[5])

#     # # 「僧侶」
#     # deck.insert(0, _kards[4])
#     # deck.insert(1, _kards[5])
#     # deck.insert(2, _kards[6])
#     # deck.insert(4, _kards[8])

#     # # 「騎士」
#     # deck.insert(0, _kards[5])
#     # deck.insert(1, _kards[5])
#     # deck.insert(2, _kards[6])
#     # deck.insert(3, _kards[4])
#     # deck.insert(4, _kards[3])
#     # deck.insert(5, _kards[3])
#     # deck.insert(6, _kards[3])
#     # deck.insert(7, _kards[3])

#     # # 「道化」
#     # deck.insert(0, _kards[2])
#     # deck.insert(1, _kards[2])

#     # 「兵士」
#     deck.insert(0, _kards[1])
#     deck.insert(1, _kards[1])

#     return deck
