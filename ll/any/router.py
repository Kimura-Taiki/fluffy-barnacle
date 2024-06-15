from dataclasses import dataclass, field
from typing import Callable

from ptc.bridge import Bridge, EMPTY_BRIDGE
from model.player import Player

@dataclass
class Router():
    bridge: Bridge = field(default_factory=lambda: EMPTY_BRIDGE)
    duels_async: Callable[[Player, Player], None] = lambda p1, p2: None
    guards_async: Callable[[str], None] = lambda s: None
    exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
    protects_async: Callable[[Player], None] = lambda p: None

    def bridge_injector(self) -> Bridge:
        return self.bridge
