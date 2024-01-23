from mod.const import compatible_with
from mod.core_view import CoreView
from mod.huda import Huda
from mod.taba import Taba

class HuseSuteView():
    def __init__(self, husehuda: Taba, sutehuda: Taba) -> None:
        self.husehuda = husehuda
        self.sutehuda = sutehuda

    def elapse(self) -> None:
        self.husehuda.elapse()
        self.sutehuda.elapse()
    
    def rearrange(self) -> None:
        self.husehuda.rearrange()
        self.sutehuda.rearrange()
    
    def get_hover_huda(self) -> Huda | None:
        if huda := self.sutehuda.get_hover_huda():
            return huda
        else:
            return self.husehuda.get_hover_huda()

compatible_with(cls=HuseSuteView, protocol=CoreView)