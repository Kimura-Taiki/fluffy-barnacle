from mod.const import compatible_with, joined_commands
from mod.core_view import CoreView
from mod.huda import Huda
from mod.taba import Taba

class HuseSuteView():
    def __init__(self, husehuda: Taba, sutehuda: Taba) -> None:
        self.husehuda = husehuda
        self.sutehuda = sutehuda
        self.var_rearrange = joined_commands(commands=[self.husehuda.rearrange, self.sutehuda.rearrange])

    def elapse(self) -> None:
        self.husehuda.elapse()
        self.sutehuda.elapse()
    
    def rearrange(self) -> None:
        self.var_rearrange()
        # self.husehuda.rearrange()
        # self.sutehuda.rearrange()
    
    def get_hover_huda(self) -> Huda | None:
        if huda := self.sutehuda.get_hover_huda():
            return huda
        else:
            return self.husehuda.get_hover_huda()

    def text(self, name: str="") -> str:
        return f"伏せ札{len(self.husehuda)}/捨て札{len(self.sutehuda)}"

compatible_with(cls=HuseSuteView, protocol=CoreView)
