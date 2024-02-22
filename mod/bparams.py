class BParams():
    def __init__(self) -> None:
        self.start_turn()
        self.turn_count = 1

    def start_turn(self) -> None:
        self.during_taiou = False

    def __str__(self) -> str:
        return f"BParams{vars(self)}"
