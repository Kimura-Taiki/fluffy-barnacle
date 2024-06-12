from dataclasses import dataclass
from random import shuffle
from typing import Callable

from any.locales import kames
from kard.syougun_effect import SyougunEffect
from model.in_effect_kard import InEffectKard
from model.kard import Kard
from model.kard_core import KardCore
from model.kard_id import KardID
from model.player import Player
from ptc.bridge import Bridge

@dataclass
class DefaultDeck():
    bridge: Bridge

    def inject_deck(self) -> None:
        self.bridge.board.deck.clear()
        deck = self._make_deck()
        while len(deck) > 0:
            self.bridge.board.deck.append(deck.pop(0))

    def _make_deck(self) -> list[Kard]:
        deck = self._original_deck()
        shuffle(deck)
        return deck
    
    def _original_deck(self) -> list[Kard]:
        deck: list[Kard] = [
            InEffectKard(kard_core=kc, png_file=f"dere1/{png_file}") for kc, png_file in self._deck_params()
        ]
        return deck
    
    def _deck_params(self) -> list[tuple[KardCore, str]]:
        _kcs = self._kard_cores()
        deck_params: list[tuple[KardCore, str]] = [
            (_kcs[1], "img01a"), (_kcs[1], "img01b"), (_kcs[1], "img01c"), (_kcs[1], "img01d"), 
            (_kcs[1], "img01e"), (_kcs[2], "img02a"), (_kcs[2], "img02b"), (_kcs[3], "img03a"), 
            (_kcs[3], "img03b"), (_kcs[4], "img04a"), (_kcs[4], "img04b"), (_kcs[5], "img05a"), 
            (_kcs[5], "img05b"), (_kcs[6], "img06a"), (_kcs[7], "img07a"), (_kcs[8], "img08a"), 
        ]
        return deck_params
    
    def _kard_cores(self) -> list[KardCore]:
        return [KardCore(id, name, rank, func) for id, name, rank, func in self._kc_params()]
    
    def _kc_params(self) -> list[tuple[KardID, Callable[[], str], int, Callable[[Bridge, Player], None]]]:
        print("HEEI")
        _func = lambda bridge, player: print("Hoge")
        kc_params: list[tuple[KardID, Callable[[], str], int, Callable[[Bridge, Player], None]]] = [
            (KardID.BANPEI, lambda : "(番兵)", 0, _func),
            (KardID.HEISI, lambda : kames(folder="heisi", key="name"), 1, _func),
            (KardID.DOUKE, lambda : kames(folder="douke", key="name"), 2, _func),
            (KardID.KISI, lambda : kames(folder="kisi", key="name"), 3, _func),
            (KardID.SOURYO, lambda : kames(folder="souryo", key="name"), 4, _func),
            (KardID.MAZYUTUSI, lambda : kames(folder="mazyutusi", key="name"), 5, _func),
            (KardID.SYOUGUN, lambda : kames(folder="syougun", key="name"), 6, SyougunEffect().use_func),
            (KardID.DAIZIN, lambda : kames(folder="daizin", key="name"), 7, _func),
            (KardID.HIME, lambda : kames(folder="hime", key="name"), 8, _func)
        ]
        return kc_params

def inject_deck(bridge: Bridge) -> None:
    DefaultDeck(bridge=bridge).inject_deck()