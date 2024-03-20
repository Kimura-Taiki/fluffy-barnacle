from typing import Any

class MParams():
    def __init__(self) -> None:
        self.start_duel()
        self.start_turn()

    def start_duel(self) -> None:
        self.has_yukihi = False
        self.henbou = False

    def start_turn(self) -> None:
        self.lingerings: list[Any] = []
        self.played_kougeki = False
        self.played_zenryoku = False
        self.played_syuutan = False
        self.played_standard = False
        self.played_ensin = False
        self.played_attract = False
        self.use_card_count = 0
        self.use_from_husehuda = False
        self.aura_damaged = False
        self.ninpo_used = False

    def __str__(self) -> str:
        return f"MParams{vars(self)}"
