#                 20                  40                  60                 79
from typing import Any

from mod.const import IMG_MAAI_AREA, IMG_DUST_AREA, WX, WY, screen, IMG_YATUBA_BG, UC_MAAI, UC_DUST, UC_AURA, UC_FLAIR, UC_LIFE\
    , SIMOTE, KAMITE, HANTE, compatible_with, IMG_ZYOGAI_AREA, UC_ZYOGAI, UC_SYUUTYUU\
    , TC_YAMAHUDA, TC_TEHUDA, TC_HUSEHUDA, TC_SUTEHUDA, TC_KIRIHUDA, UC_ISYUKU, enforce
from mod.mikoto import Mikoto
from mod.mkt.utuwa import Utuwa
from mod.youso import Youso
from mod.controller import controller
from mod.huda import Huda
from mod.taba import Taba
from mod.delivery import Delivery, Listener
from mod.moderator import moderator
from mod.req.request import Request
from mod.mkt.mparams import MParams
from mod.bparams import BParams

class Banmen():
    def __init__(self) -> None:
        self.own_mikoto = Mikoto(hoyuusya=SIMOTE)
        self.enemy_mikoto = Mikoto(hoyuusya=KAMITE)
        self.maai = Utuwa(img=IMG_MAAI_AREA, hoyuusya=HANTE, osame=10, x=WX-200, y=310, max=10)
        self.dust = Utuwa(img=IMG_DUST_AREA, hoyuusya=HANTE, osame=0, x=WX-30, y=310)
        self.zyogai = Utuwa(img=IMG_ZYOGAI_AREA, hoyuusya=HANTE, osame=50)
        li: list[Listener] = [self.own_mikoto, self.enemy_mikoto, self.maai, self.dust]
        self.listeners: list[Listener] = [item for sublist in [i.tenko() for i in li] for item in sublist]
        for listener in self.listeners:
            listener.delivery = self
        self.tabas = [listener for listener in self.listeners if isinstance(listener, Taba)]
        self.turn_player = SIMOTE
        self.b_params = BParams()

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
        moderator.stack_log()
        controller.mouse_over()

    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        huda.withdraw()
        mikoto = enforce({SIMOTE: self.own_mikoto, KAMITE: self.enemy_mikoto}.get(huda.hoyuusya), Mikoto)
        taba = enforce({TC_YAMAHUDA: mikoto.yamahuda, TC_TEHUDA: mikoto.tehuda, TC_HUSEHUDA: mikoto.husehuda,
                         TC_SUTEHUDA: mikoto.sutehuda, TC_KIRIHUDA: mikoto.kirihuda}.get(taba_code), Taba)
        taba.append(huda)
        for gottenon in mikoto.gottena:
            gottenon.redraw_img_text()

    def can_ouka_to_ryouiki(self, hoyuusya: int, from_mine: bool, from_code: int, to_mine: bool, to_code: int,
                             kazu: int=1) -> bool:
        from_utuwa = self._utuwa_target(hoyuusya=hoyuusya, is_mine=from_mine, utuwa_code=from_code)
        to_utuwa = self._utuwa_target(hoyuusya=hoyuusya, is_mine=to_mine, utuwa_code=to_code)
        return min(from_utuwa.osame, to_utuwa.max-to_utuwa.osame) >= kazu

    def send_ouka_to_ryouiki(
            self, hoyuusya: int,
            from_mine: bool=False, from_code: int=UC_DUST, from_huda: Any | None=None,
            to_mine: bool=False, to_code: int=UC_DUST, to_huda: Any | None=None,
            kazu: int=1) -> None:
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

    def respond(self, request: Request) -> Any | None:
        from mod.const import REQ_GET_HOVER
        if request.request_code == REQ_GET_HOVER:
            return self.get_hover()
        from mod.req.req_ouka import ReqOuka
        if isinstance(request, ReqOuka):
            return self._utuwa_target(hoyuusya=request.hoyuusya, is_mine=request.is_mine, utuwa_code=request.utuwa_code).osame
        from mod.req.req_taba import ReqTaba
        if isinstance(request, ReqTaba):
            return None
        return None

    def _utuwa_target(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> Utuwa:
        mikoto = self._mikoto_target(hoyuusya=hoyuusya, is_mine=is_mine)
        target = enforce({UC_MAAI: self.maai, UC_DUST: self.dust, UC_ZYOGAI: self.zyogai, UC_AURA: mikoto.aura,
                           UC_FLAIR: mikoto.flair, UC_LIFE: mikoto.life, UC_SYUUTYUU: mikoto.syuutyuu,
                           UC_ISYUKU: mikoto.isyuku}.get(utuwa_code), Utuwa)
        return target
    
    def taba_target(self, hoyuusya: int, is_mine: bool, taba_code: int) -> Taba:
        mikoto = self._mikoto_target(hoyuusya=hoyuusya, is_mine=is_mine)
        target = enforce({TC_YAMAHUDA: mikoto.yamahuda, TC_TEHUDA: mikoto.tehuda, TC_HUSEHUDA: mikoto.husehuda,
                           TC_SUTEHUDA: mikoto.sutehuda, TC_KIRIHUDA: mikoto.kirihuda}.get(taba_code), Taba)
        return target

    def ouka_count(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> int:
        return self._utuwa_target(hoyuusya=hoyuusya, is_mine=is_mine, utuwa_code=utuwa_code).osame
    
    def hand_draw(self, hoyuusya: int, is_mine: bool) -> None:
        mikoto = self._mikoto_target(hoyuusya=hoyuusya, is_mine=is_mine)
        draw_huda = mikoto.yamahuda[0]
        self.send_huda_to_ryouiki(huda=draw_huda, is_mine=True, taba_code=TC_TEHUDA)

    def _mikoto_target(self, hoyuusya: int, is_mine: bool) -> Mikoto:
        tpl = (hoyuusya, is_mine)
        return self.own_mikoto if (tpl == (SIMOTE, True)) or (tpl == (KAMITE, False)) else self.enemy_mikoto

    def m_params(self, hoyuusya: int) -> MParams:
        mikoto = enforce({SIMOTE: self.own_mikoto, KAMITE: self.enemy_mikoto}.get(hoyuusya), Mikoto)
        return mikoto.m_params



compatible_with(obj=Banmen(), protocol=Delivery)