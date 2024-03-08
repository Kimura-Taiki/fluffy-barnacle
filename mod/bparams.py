class BParams():
    def __init__(self) -> None:
        self.start_turn()
        self.turn_count = 1
        self.tatuzin_no_maai = 2
        self.tehuda_max = 4
        self.damage_attr = 0

    def start_turn(self) -> None:
        self.during_kougeki = False
        self.during_taiou = False
        self.attack_megami = -1

    def __str__(self) -> str:
        return f"BParams{vars(self)}"
