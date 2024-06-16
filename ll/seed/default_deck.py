from dataclasses import dataclass
from random import shuffle
from typing import Callable

from any.locales import kames
from kard.douke_effect import DoukeEffect
from kard.heisi_effect import HeisiEffect
from kard.kisi_effect import KisiEffect
from kard.souryo_effect import SouryoEffect
from kard.syougun_effect import SyougunEffect
from kard.mazyutusi_effect import MazyutusiEffect
from model.in_effect_kard import InEffectKard
from model.kard import Kard
from model.kard_core import KardCore
from model.kard_id import KardID
from model.player import Player
from ptc.bridge import Bridge
from seed.default_router import router

heisi_effect = HeisiEffect(
    guards_async=router.guards_async,
    arrests_async=router.arrests_async
)
douke_effect = DoukeEffect(
    guards_async=router.guards_async,
    peeps_async=router.peeps_async
)
kisi_effect = KisiEffect(
    guards_async=router.guards_async,
    duels_async=router.duels_async
)
souryo_effect = SouryoEffect(
    protects_async=router.protects_async,
)
mazyutusi_effect = MazyutusiEffect(
    guards_async=router.guards_async,
)
syougun_effect = SyougunEffect(
    guards_async=router.guards_async,
    exchange_kards_async=router.exchange_kards_async
)

@dataclass
class DefaultDeck():
    bridge: Bridge

    def inject_deck(self) -> None:
        router.bridge = self.bridge
        self.bridge.board.deck.clear()
        deck = self._make_deck()
        while len(deck) > 0:
            self.bridge.board.deck.append(deck.pop(0))

    def _make_deck(self) -> list[Kard]:
        deck = self._original_deck()
        dou1 = deck[5]
        dou2 = deck[6]
        # kis1 = deck[7]
        # kis2 = deck[8]
        pri1 = deck[9]
        # pri2 = deck[10]
        # wiz1 = deck[11]
        # wiz2 = deck[12]
        shuffle(deck)
        deck.insert(0, pri1)
        # deck.insert(1, pri2)
        deck.insert(4, dou1)
        deck.insert(5, dou2)
        # deck.insert(0, wiz1)
        # deck.insert(1, wiz2)
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
        _func = lambda bridge, player: print("Hoge")
        kc_params: list[tuple[KardID, Callable[[], str], int, Callable[[Bridge, Player], None]]] = [
            (KardID.BANPEI, lambda : "(番兵)", 0, _func),
            # (KardID.HEISI, lambda : kames(folder="heisi", key="name"), 1, _func),
            (KardID.HEISI, lambda : kames(folder="heisi", key="name"), 1, heisi_effect.use_func),
            (KardID.DOUKE, lambda : kames(folder="douke", key="name"), 2, douke_effect.use_func),
            (KardID.KISI, lambda : kames(folder="kisi", key="name"), 3, kisi_effect.use_func),
            (KardID.SOURYO, lambda : kames(folder="souryo", key="name"), 4, souryo_effect.use_func),
            (KardID.MAZYUTUSI, lambda : kames(folder="mazyutusi", key="name"), 5, mazyutusi_effect.use_func),
            (KardID.SYOUGUN, lambda : kames(folder="syougun", key="name"), 6, syougun_effect.use_func),
            (KardID.DAIZIN, lambda : kames(folder="daizin", key="name"), 7, _func),
            (KardID.HIME, lambda : kames(folder="hime", key="name"), 8, _func)
        ]
        return kc_params

def inject_deck(bridge: Bridge) -> None:
    DefaultDeck(bridge=bridge).inject_deck()