from copy import deepcopy
from random import shuffle

from model.kard import Kard
from model.in_effect_kard import InEffectKard
from model.kard_core import KardCore

_kc_params: list[tuple[str, int]] = [
    ("(番兵)", 0), ("兵士", 1), ("道化", 2), ("騎士", 3), ("僧侶", 4),
    ("魔術師", 5), ("将軍", 6), ("大臣", 7), ("姫", 8)
]
_kcs = [KardCore(name, rank) for name, rank in _kc_params]
_deck_params: list[tuple[KardCore, str]] = [
    (_kcs[1], "img01a"), (_kcs[1], "img01b"), (_kcs[1], "img01c"), (_kcs[1], "img01d"), 
    (_kcs[1], "img01e"), (_kcs[2], "img02a"), (_kcs[2], "img02b"), (_kcs[3], "img03a"), 
    (_kcs[3], "img03b"), (_kcs[4], "img04a"), (_kcs[4], "img04b"), (_kcs[5], "img05a"), 
    (_kcs[5], "img05b"), (_kcs[6], "img06a"), (_kcs[7], "img07a"), (_kcs[8], "img08a"), 
]
_deck = [InEffectKard(kard_core=kc, png_file=f"dere1/{png_file}") for kc, png_file in _deck_params]

KARD_BANPEI = InEffectKard(kard_core=_kcs[0], png_file="")
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

    # # 「兵士」
    # deck.insert(0, _kards[1])
    # deck.insert(1, _kards[1])
    # deck.insert(4, _kards[4])

    return deck
