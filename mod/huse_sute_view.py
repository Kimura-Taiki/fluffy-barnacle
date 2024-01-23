from mod.const import compatible_with
from mod.core_view import CoreView
from mod.huda import Huda

class HuseSuteView():
    def __init__(self) -> None:
        pass
        # super().__init__()

    def elapse(self) -> None:
        pass
        # return super().elapse()
    
    def rearrange(self) -> None:
        pass
        # return super().rearrange()
    
    def get_hover_huda(self) -> Huda | None:
        pass
        # return super().get_hover_huda()

compatible_with(cls=HuseSuteView, protocol=CoreView)