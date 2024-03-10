#                 20                  40                  60                 79
from typing import Callable

class BParams():
    def __init__(self, maai_func: Callable[[], int] | None=None,
                 tatuzin_func: Callable[[], int] | None=None) -> None:
        self.start_turn()
        self.turn_count = 1
        self._maai_func = maai_func if maai_func else self._default_maai_func
        self._tatuzin_no_maai = 2
        self._tatuzin_func = tatuzin_func if tatuzin_func else self._default_tatuzin_func
        self.tehuda_max = 4
        self.damage_attr = 0

    def start_turn(self) -> None:
        self.during_kougeki = False
        self.during_kirihuda = False
        self.during_taiou = False
        self.attack_megami = -1

    @property
    def tatuzin_no_maai(self) -> int:
        return self._tatuzin_func()
    
    @property
    def maai(self) -> int:
        return self._maai_func()

    def __str__(self) -> str:
        return f"BParams{vars(self)}"
    
    def _default_tatuzin_func(self) -> int:
        return self._tatuzin_no_maai
    
    def _default_maai_func(self) -> int:
        return 0
