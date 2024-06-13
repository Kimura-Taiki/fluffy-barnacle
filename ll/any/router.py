from dataclasses import dataclass
from typing import Callable

from model.player import Player

@dataclass
class Router():
    guards_async: Callable[[str], None] = lambda s: None
    exchange_kards_async: Callable[[Player, Player], None] = lambda p1, p2: None
