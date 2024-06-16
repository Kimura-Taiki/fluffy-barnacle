from dataclasses import dataclass
from typing import Callable

from model.player import Player
from ptc.bridge import Bridge

@dataclass
class Effect():
    use_func: Callable[[Bridge, Player], None] = lambda bridge, player: None
    drawn_func: Callable[[Bridge, Player], None] = lambda bridge, player: None
    discard_func: Callable[[Bridge, Player], None] = lambda bridge, player: None