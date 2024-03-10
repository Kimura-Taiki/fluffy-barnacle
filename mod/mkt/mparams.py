from typing import Any

class MParams():
    def __init__(self) -> None:
        self.start_turn()

    def start_turn(self) -> None:
        self.played_zenryoku = False
        self.played_syuutan = False
        self.played_standard = False
        self.use_card_count = 0
        self.lingerings: list[Any] = []

    def __str__(self) -> str:
        return f"MParams{vars(self)}"
