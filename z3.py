from dataclasses import dataclass

@dataclass
class Kard:
    name: str
    rank: int

@dataclass
class Player:
    name: str
    hands: list[Kard]
    alive: bool

@dataclass
class Board:
    players: list[Player]
