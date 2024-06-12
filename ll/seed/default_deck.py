from copy import deepcopy
from random import shuffle
from typing import Callable

from model.board import Board
from model.in_effect_kard import InEffectKard
from model.kard import Kard
from model.kard_core import KardCore
from model.player import Player
from ptc.bridge import Bridge

_func = lambda bridge, player: print("Hoge")

_kc_params: list[tuple[str, int, Callable[[Bridge, Player], None]]] = [
    ("(番兵)", 0, _func), ("兵士", 1, _func), ("道化", 2, _func),
    ("騎士", 3, _func), ("僧侶", 4, _func), ("魔術師", 5, _func),
    ("将軍", 6, _func), ("大臣", 7, _func), ("姫", 8, _func)
]
_kcs = [KardCore(name, rank, func) for name, rank, func in _kc_params]
_deck_params: list[tuple[KardCore, str]] = [
    (_kcs[1], "img01a"), (_kcs[1], "img01b"), (_kcs[1], "img01c"), (_kcs[1], "img01d"), 
    (_kcs[1], "img01e"), (_kcs[2], "img02a"), (_kcs[2], "img02b"), (_kcs[3], "img03a"), 
    (_kcs[3], "img03b"), (_kcs[4], "img04a"), (_kcs[4], "img04b"), (_kcs[5], "img05a"), 
    (_kcs[5], "img05b"), (_kcs[6], "img06a"), (_kcs[7], "img07a"), (_kcs[8], "img08a"), 
]
_deck: list[Kard] = [InEffectKard(kard_core=kc, png_file=f"dere1/{png_file}") for kc, png_file in _deck_params]

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

def _make_deck(bridge: Bridge) -> list[Kard]:
    deck = deepcopy(_deck)
    shuffle(deck)
    return deck

def inject_deck(bridge: Bridge) -> None:
    bridge.board.deck.clear()
    deck = _make_deck(bridge=bridge)
    while len(deck) > 0:
        bridge.board.deck.append(deck.pop(0))
    
