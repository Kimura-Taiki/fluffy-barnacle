from copy import deepcopy
from random import shuffle

from model.kard import Kard

_kard0 = Kard(name="(番兵)", rank=0, png_file="")
# _kard1 = Kard(name="兵士", rank=1, png_file="img1")
# _kard2 = Kard(name="道化", rank=2, png_file="img2")
# _kard3 = Kard(name="騎士", rank=3, png_file="img3")
# _kard4 = Kard(name="僧侶", rank=4, png_file="img4")
# _kard5 = Kard(name="魔術師", rank=5, png_file="img5")
# _kard6 = Kard(name="将軍", rank=6, png_file="img6")
# _kard7 = Kard(name="大臣", rank=7, png_file="img7")
# _kard8 = Kard(name="姫", rank=8, png_file="img8")
KARD_HEISI = Kard(name="兵士", rank=1, png_file="img1")
KARD_DOUKE = Kard(name="道化", rank=2, png_file="img2")
KARD_KISI = Kard(name="騎士", rank=3, png_file="img3")
KARD_SOURYO = Kard(name="僧侶", rank=4, png_file="img4")
KARD_MAZYUTUSI = Kard(name="魔術師", rank=5, png_file="img5")
KARD_SYOUGUN = Kard(name="将軍", rank=6, png_file="img6")
KARD_DAIZIN = Kard(name="大臣", rank=7, png_file="img7")
KARD_HIME = Kard(name="姫", rank=8, png_file="img8")
_kards = [_kard0, KARD_HEISI, KARD_DOUKE, KARD_KISI, KARD_SOURYO, KARD_MAZYUTUSI, KARD_SYOUGUN, KARD_DAIZIN, KARD_HIME]
_ids = [1]*5+[2, 3, 4, 5]*2+[6, 7, 8]

def make_deck() -> list[Kard]:
    deck = [deepcopy(_kards[i]) for i in _ids]
    shuffle(deck)

    # # 「姫」の処理を実装する為に１枚目を姫に修正
    # deck.insert(0, _kards[8])

    # # 「大臣」の処理を実装する為に１枚目を大臣に修正
    # deck.insert(0, _kards[7])
    # deck.insert(1, _kards[7])
    # deck.insert(4, _kards[8])
    # deck.insert(5, _kards[1])

    # # 「将軍」の処理を実装する為に１枚目を将軍に変更
    # deck.insert(0, _kards[6])

    # # 「魔術師」
    # deck.insert(0, _kards[5])
    # deck.insert(1, _kards[8])
    # deck.insert(2, _kards[5])

    # # 「僧侶」
    # deck.insert(0, _kards[4])
    # deck.insert(1, _kards[5])
    # deck.insert(2, _kards[6])
    # deck.insert(4, _kards[8])

    # 「騎士」
    deck.insert(0, _kards[3])
    deck.insert(1, _kards[5])
    deck.insert(2, _kards[6])
    deck.insert(3, _kards[4])
    deck.insert(4, _kards[5])

    return deck
