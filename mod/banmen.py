from mod.const import IMG_MAAI_AREA, IMG_DUST_AREA, WX, WY, screen, IMG_YATUBA_BG, UC_MAAI, UC_DUST, UC_AURA, UC_FLAIR, UC_LIFE\
    , SIMOTE, KAMITE, HANTE
from mod.mikoto import Mikoto
from mod.utuwa import Utuwa
from mod.youso import Youso
from mod.controller import controller
from mod.huda import Huda

class Banmen():
    def __init__(self) -> None:
        self.own_mikoto = Mikoto(hoyuusya=SIMOTE)
        self.enemy_mikoto = Mikoto(hoyuusya=KAMITE)
        self.maai = Utuwa(img=IMG_MAAI_AREA, hoyuusya=HANTE, num=10, x=WX-200, y=310, max=10)
        self.dust = Utuwa(img=IMG_DUST_AREA, hoyuusya=HANTE, num=0, x=WX-30, y=310)

    def get_hover(self) -> Youso | None:
        if y1 := self.own_mikoto.get_hover():
            return y1
        else:
            return self.enemy_mikoto.get_hover()

    def elpase(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
        self.own_mikoto.elapse()
        self.enemy_mikoto.elapse()
        self.maai.draw()
        self.dust.draw()
        controller.mouse_over()

    # def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
    #     huda.withdraw()
    #     match taba_code:
    #         case TC_HUSEHUDA:
    #             self.husehuda.append(huda)
    #     for gottenon in self.gottena:
    #         gottenon.redraw_img_text()

    def can_move_ouka(self, utuwa: Utuwa, is_mine: bool, utuwa_code: int, kazu: int=1) -> bool:
        if utuwa.num < kazu:
            return False
        target = self._utuwa_target(utuwa=utuwa, is_mine=is_mine, utuwa_code=utuwa_code)
        return target.max-target.num >= kazu

    def send_ouka_to_ryouiki(self, utuwa: Utuwa, is_mine: bool, utuwa_code: int, kazu: int=1) -> None:
        target = self._utuwa_target(utuwa=utuwa, is_mine=is_mine, utuwa_code=utuwa_code)
        real_shift = min(kazu, utuwa.num, target.max-target.num)
        utuwa.num -= real_shift
        target.num += real_shift

    def _utuwa_target(self, utuwa: Utuwa, is_mine: bool, utuwa_code: int) -> Utuwa:
        tpl = (utuwa.hoyuusya, is_mine)
        mikoto = self.own_mikoto if (tpl == (SIMOTE, True)) or (tpl == (KAMITE, False)) else self.enemy_mikoto
        if not (target := {UC_MAAI: self.maai, UC_DUST: self.dust, UC_AURA: mikoto.aura, UC_FLAIR: mikoto.flair, UC_LIFE: mikoto.life
                  }.get(utuwa_code)):
            raise ValueError(f"Invalid utuwa_code: {utuwa_code}")
        return target
