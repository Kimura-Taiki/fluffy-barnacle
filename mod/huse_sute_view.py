from mod.const import compatible_with
from mod.core_view import CoreView
from mod.huda import Huda
from mod.taba import Taba, DuckTaba

class HuseSuteView():
    def __init__(self, husehuda: Taba=DuckTaba(), sutehuda: Taba=DuckTaba(), is_own: bool=True) -> None:
        self.husehuda = husehuda
        self.sutehuda = sutehuda
        self.is_own = is_own

    def elapse(self) -> None:
        self.husehuda.elapse()
        self.sutehuda.elapse()
        
    def get_hover_huda(self) -> Huda | None:
        if huda := self.sutehuda.get_hover_huda():
            return huda
        else:
            return self.husehuda.get_hover_huda()

    def text(self, name: str="") -> str:
        return f"伏せ札{len(self.husehuda)}/捨て札{len(self.sutehuda)}"

compatible_with(obj=HuseSuteView(), protocol=CoreView)
