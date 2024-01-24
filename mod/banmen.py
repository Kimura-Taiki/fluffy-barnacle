from mod.const import IMG_MAAI_AREA, IMG_DUST_AREA, WX, WY, screen, IMG_YATUBA_BG
from mod.mikoto import Mikoto
from mod.utuwa import Utuwa
from mod.youso import Youso
from mod.controller import controller
from mod.huda import Huda

class Banmen():
    def __init__(self) -> None:
        self.own_mikoto = Mikoto(is_own=True)
        self.enemy_mikoto = Mikoto(is_own=False)
        self.maai = Utuwa(img=IMG_MAAI_AREA, is_own=True, num=10, x=WX-200, y=310, max=10)
        self.dust = Utuwa(img=IMG_DUST_AREA, is_own=True, num=0, x=WX-30, y=310)

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

    # def can_move_ouka(self, utuwa: Utuwa, is_mine: bool, utuwa_code: int, kazu: int=1) -> bool:
    #     if utuwa.num < kazu:
    #         return False
        

    # def send_ouka_to_ryouiki(self, utuwa: Utuwa, kazu: int, is_mine: bool, utuwa_code: int) -> None:
    #     move = min(utuwa.num, kazu)
