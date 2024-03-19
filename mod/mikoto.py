#                 20                  40                  60                 79
from mod.const import WX, WY, IMG_AURA_AREA, IMG_FLAIR_AREA, IMG_LIFE_AREA,\
    IMG_SYUUTYUU_AREA, compatible_with, SIMOTE, KAMITE, IMG_ISYUKU_AREA
from mod.mkt.gottenon import Gottenon
from mod.mkt.gottena import Gottena
from mod.mkt.utuwa import Utuwa
from mod.tf.yamahuda import yamahuda_factory
from mod.tf.tehuda import tehuda_factory
from mod.tf.husehuda import husehuda_factory
from mod.tf.sutehuda import sutehuda_factory
from mod.tf.kirihuda import kirihuda_factory
from mod.mkt.huse_sute_view import HuseSuteView
from mod.delivery import Listener, Delivery, duck_delivery
from mod.youso import Youso
from mod.mkt.mparams import MParams
from mod.mkt.syuutyuu import syuutyuu_utuwa

class Mikoto():
    def __init__(self, hoyuusya: int) -> None:
        self.delivery: Delivery = duck_delivery
        self.hoyuusya = hoyuusya
        self.m_params = MParams()
        self.husehuda = husehuda_factory.maid_by_cards(cards=[], hoyuusya=hoyuusya)
        self.sutehuda = sutehuda_factory.maid_by_cards(cards=[], hoyuusya=hoyuusya)
        if hoyuusya == SIMOTE:
            self._simote_make()
        elif hoyuusya == KAMITE:
            self._kamite_make()
        self.gottena = Gottena(data=[Gottenon(core_view=self.yamahuda, name="山札", x=140, y=WY-210),
                                     Gottenon(core_view=self.tehuda, name="手札", x=140, y=WY-150),
                                     Gottenon(core_view=HuseSuteView(husehuda=self.husehuda, sutehuda=self.sutehuda, hoyuusya=hoyuusya),
                                              name="伏せ札・捨て札", x=140, y=WY-90),
                                     Gottenon(core_view=self.kirihuda, name="切り札", x=140, y=WY-30)])
        self.syuutyuu = syuutyuu_utuwa(hoyuusya=self.hoyuusya, osame=0, x=310, y=WY-210)
        self.isyuku = Utuwa(img=IMG_ISYUKU_AREA, hoyuusya=self.hoyuusya, osame=0, x=330, y=WY-210, max=1)
        self.aura = Utuwa(img=IMG_AURA_AREA, hoyuusya=self.hoyuusya, osame=3, x=310, y=WY-150, max=5)
        self.flair = Utuwa(img=IMG_FLAIR_AREA, hoyuusya=self.hoyuusya, osame=0, x=310, y=WY-90)
        self.life = Utuwa(img=IMG_LIFE_AREA, hoyuusya=self.hoyuusya, osame=10, x=310, y=WY-30)
        self.utuwas = [self.syuutyuu, self.aura, self.flair, self.life]
        for listener in self.tenko():
            listener.hoyuusya = self.hoyuusya

    def elapse(self) -> None:
        self.gottena.selected.core_view.elapse()
        self.gottena.elapse()
        self.syuutyuu.draw()
        if self.isyuku.osame:
            self.isyuku.isyuku_draw()
        self.aura.draw()
        self.flair.draw()
        self.life.draw()

    def get_hover(self) -> Youso | None:
        if y1 := self.gottena.get_hover_gotten():
            return y1
        if y2 := next((utuwa for utuwa in self.utuwas if utuwa.is_cursor_on()), None):
            return y2
        else:
            return self.gottena.selected.core_view.get_hover_huda()

    def tenko(self) -> list[Listener]:
        li: list[Listener] = [self.yamahuda, self.tehuda, self.husehuda, self.sutehuda, self.kirihuda, self.syuutyuu, self.aura, self.flair, self.life]
        return [self]+[item for sublist in [i.tenko() for i in li] for item in sublist]

    def __repr__(self) -> str:
        obj_type = type(self).__name__
        obj_address = hex(id(self))
        return f"<{obj_type} object at {obj_address}>"

    def _simote_make(self) -> None:
        from kaiketus import m00a, m00b
        # self.m_params.has_yukihi = True
        from kaiketus.m08o import n_1, n_2, n_3, n_4, n_5, n_6#, n_7, s_1, s_2, s_3, s_4
        hands = [m00b.n_4, m00b.n_5, m00b.n_6, n_1, n_2, n_3, n_4, n_5, n_6]#, n_7]
        trumps = [m00b.s_3, m00a.s_3, m00a.s_2]#, s_1, s_2, s_3, s_4]
        self.yamahuda = yamahuda_factory.maid_by_cards(cards=[], hoyuusya=self.hoyuusya)
        self.tehuda = tehuda_factory.maid_by_cards(cards=hands, hoyuusya=self.hoyuusya)
        self.kirihuda = kirihuda_factory.maid_by_cards(cards=trumps, hoyuusya=self.hoyuusya)

    def _kamite_make(self) -> None:
        from kaiketus import m00a, m00b
        from kaiketus.m01o import n_1, n_2, n_3, n_4, n_5, n_6, n_7, s_1, s_2, s_3, s_4
        self.yamahuda = yamahuda_factory.maid_by_cards(cards=[n_5, n_6, n_7], hoyuusya=self.hoyuusya)
        self.tehuda = tehuda_factory.maid_by_cards(cards=[n_1, n_2, n_3, n_4, m00b.n_5, m00b.n_9], hoyuusya=self.hoyuusya)
        self.kirihuda = kirihuda_factory.maid_by_cards(cards=[s_1, s_2, s_3, s_4], hoyuusya=self.hoyuusya)

compatible_with(obj=Mikoto(hoyuusya=SIMOTE), protocol=Listener)
