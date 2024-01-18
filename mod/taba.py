from mod.huda import Huda

class Taba(list[Huda]):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__([setattr(huda, 'belongs_to', self) or huda for huda in data])
        self.other_params: list[int] = []
