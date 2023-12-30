from mod.huda import Huda
from mod.taba import Taba

# taba = Taba(data=[Huda(screen=screen, img=UTURO(i+1), angle=HAND_ANGLE(i), scale=0.6, x=HAND_X(i), y=HAND_Y(i)) for i in range(CARDS)])

class Tehuda(Taba):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__(data)

    # @classmethod
    # def made_by_files(strs: list[str]) -> "Tehuda":
