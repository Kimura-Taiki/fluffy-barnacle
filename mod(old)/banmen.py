#                 20                  40                  60                 79
from typing import runtime_checkable, Protocol

from mod.const import IMG_MAAI_AREA, IMG_DUST_AREA, WX, WY, screen, IMG_YATUBA_BG,\
    UC_MAAI, UC_DUST, UC_AURA, UC_FLAIR, UC_LIFE, UC_ISYUKU,\
    SIMOTE, KAMITE, HANTE, compatible_with, IMG_ZYOGAI_AREA,\
    UC_ZYOGAI, UC_SYUUTYUU, USAGE_DEPLOYED, CT_HUYO,\
    TC_MISIYOU, TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, enforce, USAGE_USED, CT_KOUDOU, UC_TATUZIN\
    , opponent, MS_MINCHO_COL, BLACK, SC_MAAI, SC_TATUZIN
from mod.classes import Callable, Any, Card, Youso, Huda, Taba, Delivery, moderator, controller
from mod.delivery import Listener
from mod.mikoto import Mikoto
from mod.mkt.utuwa import Utuwa
from mod.mkt.mparams import MParams
from mod.bparams import BParams
from mod.coous.continuous import Continuous, _Card
from mod.banmen_draw import maai_draw, tatuzin_draw, dust_draw
from mod.coous.scalar_correction import applied_scalar

class Banmen():
    def __init__(self) -> None:
        self.own_mikoto = Mikoto(hoyuusya=SIMOTE)
        self.enemy_mikoto = Mikoto(hoyuusya=KAMITE)
        self.maai = Utuwa(img=IMG_MAAI_AREA, hoyuusya=HANTE, osame=10, x=WX-200, y=310, max=10)
        self.maai.draw = lambda: maai_draw(self.maai)
        self.dust = Utuwa(img=IMG_DUST_AREA, hoyuusya=HANTE, osame=0, x=WX-30, y=310)
        self.dust.draw = lambda: dust_draw(self.dust)
        self.zyogai = Utuwa(img=IMG_ZYOGAI_AREA, hoyuusya=HANTE, osame=50)
        li: list[Listener] = [self.own_mikoto, self.enemy_mikoto, self.maai, self.dust]
        self.listeners: list[Listener] = [item for sublist in [i.tenko() for i in li] for item in sublist]
        for listener in self.listeners:
            listener.delivery = self
        self.tabas = [listener for listener in self.listeners if isinstance(listener, Taba)]
        self.turn_player = SIMOTE
        self.b_params = BParams(maai_func=self._maai_func, tatuzin_func=self._tatuzin_func)

    def get_hover(self) -> Youso | None:
        if y2 := self.own_mikoto.get_hover():
            return y2
        else:
            return self.enemy_mikoto.get_hover()

    def elpase(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        self.own_mikoto.elapse()
        self.enemy_mikoto.elapse()
        self.maai.draw()
        self.dust.draw()
        tatuzin_draw(dest=(WX-300, 360), value=self.b_params.tatuzin_no_maai)
        moderator.stack_log()
        controller.mouse_over()

    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int, is_top: bool=False) -> None:
        huda.withdraw()
        mikoto = enforce({SIMOTE: self.own_mikoto, KAMITE: self.enemy_mikoto}.get(huda.hoyuusya), Mikoto)
        taba = self.taba(hoyuusya=huda.hoyuusya if is_mine else opponent(huda.hoyuusya), taba_code=taba_code)
        if is_top:
            taba.insert(0, huda)
        else:
            taba.append(huda)
        if is_mine == False:
            huda.hoyuusya = opponent(huda.hoyuusya)
        for gottenon in mikoto.gottena:
            gottenon.redraw_img_text()

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int,
                             kazu: int=1) -> bool:
        from_utuwa = self._utuwa_target(hoyuusya=hoyuusya, is_mine=from_mine, utuwa_code=from_code)
        to_utuwa = self._utuwa_target(hoyuusya=hoyuusya, is_mine=to_mine, utuwa_code=to_code)
        return min(from_utuwa.osame, to_utuwa.max-to_utuwa.osame) >= kazu

    def send_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool=False,
    from_code: int=UC_DUST, from_huda: Any | None=None, to_mine: bool=False,
    to_code: int=UC_DUST, to_huda: Any | None=None, kazu: int=1) -> None:
        from_utuwa = from_huda if isinstance(
            from_huda, Youso) else self._utuwa_target(
                hoyuusya=hoyuusya, is_mine=from_mine, utuwa_code=from_code)
        to_utuwa = to_huda if isinstance(
            to_huda, Youso) else self._utuwa_target(
                hoyuusya=hoyuusya, is_mine=to_mine, utuwa_code=to_code)
        real_shift = min(kazu, from_utuwa.osame, to_utuwa.max-to_utuwa.osame)
        from_utuwa.osame -= real_shift
        to_utuwa.osame += real_shift

    def inject_main_phase(self) -> None:
        from mod.popup_message import popup_message
        # popup_message.add("Inject Main Phase")
        for taba in self.tabas:
            taba.inject_kwargs(taba.main_phase_inject_kwargs)

    def inject_view(self) -> None:
        from mod.popup_message import popup_message
        # popup_message.add("Inject View")
        for taba in self.tabas:
            taba.inject_kwargs(taba.view_inject_kwargs)

    def utuwa_target(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> Any:
        return self._utuwa_target(hoyuusya=hoyuusya, is_mine=is_mine, utuwa_code=utuwa_code) 

    def _utuwa_target(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> Utuwa:
        mikoto = self._mikoto_target(hoyuusya=hoyuusya, is_mine=is_mine)
        target = enforce({UC_MAAI: self.maai, UC_DUST: self.dust, UC_ZYOGAI: self.zyogai, UC_AURA: mikoto.aura,
                           UC_FLAIR: mikoto.flair, UC_LIFE: mikoto.life, UC_SYUUTYUU: mikoto.syuutyuu,
                           UC_ISYUKU: mikoto.isyuku}.get(utuwa_code), Utuwa)
        return target

    def taba(self, hoyuusya: int, taba_code: int) -> Taba:
        mikoto = self._mikoto_target(hoyuusya=hoyuusya, is_mine=True)
        taba = enforce({TC_MISIYOU: mikoto.misiyou, TC_YAMAHUDA: mikoto.yamahuda, TC_TEHUDA: mikoto.tehuda,
                        TC_HUSEHUDA: mikoto.husehuda, TC_SUTEHUDA: mikoto.sutehuda, TC_KIRIHUDA: mikoto.kirihuda
                        }.get(taba_code), Taba)
        return taba

    def ouka_count(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> int:
        if utuwa_code == UC_TATUZIN:
            return self.b_params.tatuzin_no_maai
        return self._utuwa_target(hoyuusya=hoyuusya, is_mine=is_mine, utuwa_code=utuwa_code).osame
    
    def _mikoto_target(self, hoyuusya: int, is_mine: bool) -> Mikoto:
        tpl = (hoyuusya, is_mine)
        return self.own_mikoto if (tpl == (SIMOTE, True)) or (tpl == (KAMITE, False)) else self.enemy_mikoto

    def m_params(self, hoyuusya: int) -> MParams:
        mikoto = enforce({SIMOTE: self.own_mikoto, KAMITE: self.enemy_mikoto}.get(hoyuusya), Mikoto)
        return mikoto.m_params

    def is_duck(self) -> bool:
        return False

    def _tatuzin_func(self) -> int:
        return applied_scalar(i=self.b_params._tatuzin_no_maai, scalar=SC_TATUZIN, delivery=self)

    def _maai_func(self) -> int:
        return applied_scalar(i=self.ouka_count(hoyuusya=SIMOTE, is_mine=False, utuwa_code=UC_MAAI),
                              scalar=SC_MAAI, delivery=self)

    def cfs(self, type: int, hoyuusya: int, card: _Card) -> list[Continuous]:
        st = self.taba(hoyuusya=hoyuusya, taba_code=TC_SUTEHUDA)
        sf = self.taba(hoyuusya=opponent(hoyuusya), taba_code=TC_SUTEHUDA)
        kt = self.taba(hoyuusya=hoyuusya, taba_code=TC_KIRIHUDA)
        kf = self.taba(hoyuusya=opponent(hoyuusya), taba_code=TC_KIRIHUDA)
        def is_deployed(huda: Huda) -> bool:
            return huda.card.type == CT_HUYO and huda.usage == USAGE_DEPLOYED
        def is_used(huda: Huda) -> bool:
            return huda.usage == USAGE_USED
        # def is_d_and_u(huda: Huda) -> bool:
        #     return is_deployed(huda) or is_used(huda)
        def is_cond(cf: Continuous, huda: Huda) -> bool:
            return cf.type == type and cf.cond(self, hoyuusya, huda.hoyuusya, card)
        def get_filtered_cfs(hudas: list[Huda], func: Callable[[Huda], bool]) -> list[Continuous]:
            return [cf for huda in hudas if func(huda) for cf in huda.card.cfs if is_cond(cf, huda)]
        def get_filtered_used(hudas: list[Huda], func: Callable[[Huda], bool]) -> list[Continuous]:
            return [cf for huda in hudas if func(huda) for cf in huda.card.used if is_cond(cf, huda)]
        def is_cond_mikoto(cf: Continuous, mikoto: int) -> bool:
            return cf.type == type and cf.cond(self, hoyuusya, mikoto, card)
        # (st_cfs, sf_cfs, kt_cfs, kf_cfs) = [get_filtered_cfs(hudas, func) for hudas, func in [
        #     (st, is_deployed), (sf, is_deployed), (kt, is_d_and_u), (kf, is_d_and_u)
        # ]]
        (st_cfs, sf_cfs, kt_cfs, kf_cfs, kt_used, kf_used) = [filter(hudas, func) for hudas, func, filter in [
            (st, is_deployed, get_filtered_cfs), (sf, is_deployed, get_filtered_cfs),
            (kt, is_deployed, get_filtered_cfs), (kf, is_deployed, get_filtered_cfs),
            (kt, is_used, get_filtered_used), (kf, is_used, get_filtered_used)
        ]]
        lt = self.m_params(hoyuusya).lingerings
        lt_cfs = [enforce(cf, Continuous) for cf in lt if is_cond_mikoto(enforce(cf, Continuous), hoyuusya)]
        lf = self.m_params(opponent(hoyuusya)).lingerings
        lf_cfs = [enforce(cf, Continuous) for cf in lf if is_cond_mikoto(enforce(cf, Continuous), opponent(hoyuusya))]
        return st_cfs+sf_cfs+kt_cfs+kf_cfs+kt_used+kf_used+lt_cfs+lf_cfs




compatible_with(obj=Banmen(), protocol=Delivery)