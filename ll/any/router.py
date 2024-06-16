from dataclasses import dataclass, field
from typing import Callable

from model.kard import Kard
from model.player import Player
from ptc.bridge import Bridge, EMPTY_BRIDGE

@dataclass
class Router():
    bridge: Bridge = field(default_factory=lambda: EMPTY_BRIDGE)
    arrests_async: Callable[[Player, Kard], None] = lambda p, k: None
    duels_async: Callable[[Player, Player], None] = lambda p1, p2: None
    guards_async: Callable[[str], None] = lambda s: None
    exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
    peeps_async: Callable[[Player, Player, Player], None] = lambda p1, p2, p3: None
    protects_async: Callable[[Player], None] = lambda p: None

    def bridge_injector(self) -> Bridge:
        return self.bridge
