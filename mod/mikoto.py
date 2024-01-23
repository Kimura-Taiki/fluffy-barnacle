from functools import partial

#                 20                  40                  60                 79
from mod.const import UTURO, HONOKA, CARDS, WX, WY, TC_YAMAHUDA, TC_TEHUDA\
    , TC_SUTEHUDA, TC_HUSEHUDA, TC_KIRIHUDA, TC_MISIYOU, TC_ZYOGAI, screen\
    , IMG_AURA_AREA, IMG_FLAIR_AREA, IMG_LIFE_AREA, IMG_SYUUTYUU_AREA\
    , compatible_with
from mod.gottenon import Gottenon
from mod.gottena import Gottena
from mod.yamahuda import yamahuda_made_by_files
from mod.tehuda import tehuda_made_by_files
from mod.husehuda import husehuda_made_by_files
from mod.sutehuda import sutehuda_made_by_files
from mod.huse_sute_view import HuseSuteView
from mod.huda import Huda
from mod.taba import Taba
from mod.delivery import Delivery

class Mikoto():
    def __init__(self, is_own: bool) -> None:
        self.is_own = is_own
        self.yamahuda: Taba = yamahuda_made_by_files(surfaces=[HONOKA(i) for i in range(1, 10)], delivery=self, is_own=True)
        self.tehuda: Taba = tehuda_made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)], delivery=self, is_own=True)
        self.husehuda: Taba = husehuda_made_by_files(surfaces=[HONOKA(i) for i in range(2, 4)], delivery=self, is_own=True)
        self.sutehuda: Taba = sutehuda_made_by_files(surfaces=[HONOKA(i) for i in range(4, 9)], delivery=self, is_own=True)
        self.kirihuda: Taba = tehuda_made_by_files(surfaces=[HONOKA(i) for i in range(4, 7)], delivery=self, is_own=True)
        self.gottena: Gottena = Gottena(data=[Gottenon(core_view=self.yamahuda, name="山札", x=WX-140, y=WY-210),
                                              Gottenon(core_view=self.tehuda, name="手札", x=WX-140, y=WY-150),
                                              Gottenon(core_view=HuseSuteView(husehuda=self.husehuda, sutehuda=self.sutehuda),
                                                       name="伏せ札・捨て札", x=WX-140, y=WY-90),
                                              Gottenon(core_view=self.kirihuda, name="切り札", x=WX-140, y=WY-30)])

    def elapse(self) -> None:
        self.gottena.selected.core_view.elapse()
        self.gottena.elapse()
        screen.blit(source=IMG_AURA_AREA, dest=[WX-340, WY-240])
        screen.blit(source=IMG_FLAIR_AREA, dest=[WX-340, WY-180])
        screen.blit(source=IMG_LIFE_AREA, dest=[WX-340, WY-120])
        screen.blit(source=IMG_SYUUTYUU_AREA, dest=[WX-340, WY-60])

    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        huda.withdraw()
        match taba_code:
            case TC_HUSEHUDA:
                self.husehuda.append(huda)
        for gottenon in self.gottena:
            gottenon.redraw_img_text()

compatible_with(cls=Mikoto, protocol=Delivery)