#                 20                  40                  60                 79
from mod.const import UTURO, HONOKA, CARDS, WX, WY, TC_YAMAHUDA, TC_TEHUDA\
    , TC_SUTEHUDA, TC_HUSEHUDA, TC_KIRIHUDA, TC_MISIYOU, TC_ZYOGAI, screen\
    , IMG_AURA_AREA, IMG_FLAIR_AREA, IMG_LIFE_AREA, IMG_SYUUTYUU_AREA\
    , compatible_with, HONOKA_S, draw_aiharasuu, SIMOTE
from mod.gottenon import Gottenon
from mod.gottena import Gottena
from mod.tf.yamahuda import yamahuda_factory
from mod.tf.tehuda import tehuda_factory
from mod.tf.husehuda import husehuda_factory
from mod.tf.sutehuda import sutehuda_factory
from mod.tf.kirihuda import kirihuda_factory
from mod.huse_sute_view import HuseSuteView
from mod.taba import Taba
from mod.delivery import Listener, Delivery, duck_delivery
from mod.utuwa import Utuwa
from mod.youso import Youso
from koukas.n_1 import n_1, n_2, n_3, n_4

class Mikoto():
    def __init__(self, hoyuusya: int) -> None:
        self.delivery: Delivery = duck_delivery
        self.hoyuusya = hoyuusya
        self.yamahuda: Taba = yamahuda_factory.maid_by_files(surfaces=[HONOKA(i) for i in range(1, 3)], hoyuusya=self.hoyuusya)
        # self.tehuda: Taba = tehuda_factory.maid_by_files(surfaces=[UTURO(i) for i in range(3, 7)], hoyuusya=self.hoyuusya)
        self.tehuda: Taba = tehuda_factory.maid_by_cards(cards=[n_1, n_2, n_3, n_4], hoyuusya=self.hoyuusya)
        self.husehuda: Taba = husehuda_factory.maid_by_files(surfaces=[HONOKA(i) for i in range(7, 8)], hoyuusya=self.hoyuusya)
        self.sutehuda: Taba = sutehuda_factory.maid_by_files(surfaces=[HONOKA(i) for i in range(8, 9)], hoyuusya=self.hoyuusya)
        self.kirihuda: Taba = kirihuda_factory.maid_by_files(surfaces=[HONOKA_S(i) for i in range(1, 4)], hoyuusya=self.hoyuusya)
        self.gottena = Gottena(data=[Gottenon(core_view=self.yamahuda, name="山札", x=140, y=WY-210),
                                     Gottenon(core_view=self.tehuda, name="手札", x=140, y=WY-150),
                                     Gottenon(core_view=HuseSuteView(husehuda=self.husehuda, sutehuda=self.sutehuda, hoyuusya=hoyuusya),
                                              name="伏せ札・捨て札", x=140, y=WY-90),
                                     Gottenon(core_view=self.kirihuda, name="切り札", x=140, y=WY-30)])
        self.syuutyuu = Utuwa(img=IMG_SYUUTYUU_AREA, hoyuusya=self.hoyuusya, num=0, x=310, y=WY-210, max=2)
        self.aura = Utuwa(img=IMG_AURA_AREA, hoyuusya=self.hoyuusya, num=3, x=310, y=WY-150, max=5)
        self.flair = Utuwa(img=IMG_FLAIR_AREA, hoyuusya=self.hoyuusya, num=0, x=310, y=WY-90)
        self.life = Utuwa(img=IMG_LIFE_AREA, hoyuusya=self.hoyuusya, num=10, x=310, y=WY-30)
        for listener in self.tenko():
            listener.hoyuusya = self.hoyuusya

    def elapse(self) -> None:
        self.gottena.selected.core_view.elapse()
        self.gottena.elapse()
        self.syuutyuu.draw()
        self.aura.draw()
        self.flair.draw()
        self.life.draw()

    def get_hover(self) -> Youso | None:
        if y1 := self.gottena.get_hover_gotten():
            return y1
        else:
            return self.gottena.selected.core_view.get_hover_huda()

    def tenko(self) -> list[Listener]:
        li: list[Listener] = [self.yamahuda, self.tehuda, self.husehuda, self.sutehuda, self.kirihuda, self.syuutyuu, self.aura, self.flair, self.life]
        return [self]+[item for sublist in [i.tenko() for i in li] for item in sublist]

    def __repr__(self) -> str:
        obj_type = type(self).__name__
        obj_address = hex(id(self))
        return f"<{obj_type} object at {obj_address}>"

compatible_with(obj=Mikoto(hoyuusya=SIMOTE), protocol=Listener)
