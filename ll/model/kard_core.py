from dataclasses import dataclass

@dataclass(frozen=True)
class KardCore():
    name: str
    rank: int
