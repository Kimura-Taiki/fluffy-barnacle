class MParams():
    def __init__(self) -> None:
        self.start_turn()

    def start_turn(self) -> None:
        self.played_zenryoku = False
        self.played_standard = False

    def __str__(self) -> str:
        return f"MParams{vars(self)}"
