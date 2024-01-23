from mod.core_view import CoreView
from mod.huda import Huda

class HuseSuteView(CoreView):
    def __init__(self) -> None:
        super().__init__()

    def elapse(self) -> None:
        return super().elapse()
    
    def rearrange(self) -> None:
        return super().rearrange()
    
    def get_hover_huda(self) -> Huda | None:
        return super().get_hover_huda()