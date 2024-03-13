from typing import Any

class MParams():
    def __init__(self) -> None:
        self.start_turn()

    def start_turn(self) -> None:
        self.lingerings: list[Any] = []
        self.played_zenryoku = False
        self.played_syuutan = False
        self.played_standard = False
        self.use_card_count = 0
        self.use_from_husehuda = False

    def __str__(self) -> str:
        return f"MParams{vars(self)}"
