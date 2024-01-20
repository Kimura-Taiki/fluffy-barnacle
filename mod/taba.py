from mod.huda import Huda

class Taba(list[Huda]):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__([setattr(huda, 'belongs_to', self) or huda for huda in data])
        self.other_params: list[int] = []

    def get_hover_huda(self) -> Huda | None:
        return next((huda for huda in self[::-1] if huda.is_cursor_on()), None)

    def elapse(self) -> None:
        [huda.draw() for huda in self]

    def rearrange(self) -> None:
        raise NotImplementedError("Taba.rearrange が未定義です")
