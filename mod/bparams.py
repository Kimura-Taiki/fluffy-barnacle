#                 20                  40                  60                 79
from typing import Callable, Any

class BParams():
    def __init__(self, maai_func: Callable[[], int] | None=None,
                 tatuzin_func: Callable[[], int] | None=None) -> None:
        self.turn_count = 1
        self._maai_func = maai_func if maai_func else self._default_maai_func
        self._tatuzin_no_maai = 2
        self._tatuzin_func = tatuzin_func if tatuzin_func else self._default_tatuzin_func
        self.tehuda_max = 2
        self.damage_attr = 0
        self.start_turn()

    def start_turn(self) -> None:
        self.during_kougeki = False
        self.during_kirihuda = False
        self.during_taiou = False
        self.sukinagasi = False
        self.attack_megami = -1
        self.start_turn_maai = self.maai
        self.start_phase()

    def start_phase(self) -> None:
        self.phase_ended = False

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
