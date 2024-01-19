from mod.const import UTURO, HONOKA, CARDS
from mod.gottenon import Gottenon
from mod.tehuda import Tehuda

class Mikoto():
    def __init__(self, is_own: bool) -> None:
        self.is_own = is_own
        self.yamahuda: Tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)], is_own=True)
        self.tehuda: Tehuda = Tehuda.made_by_files(surfaces=[HONOKA(i) for i in range(1, CARDS+1)], is_own=True)
        self.husesute: Tehuda
        self.kirihuda: Tehuda
        self.gottenons: list[Gottenon]
