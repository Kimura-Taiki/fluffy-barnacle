from mod.const import IMG_MAAI_AREA, IMG_DUST_AREA, WX, WY, screen, IMG_YATUBA_BG
from mod.mikoto import Mikoto
from mod.utuwa import Utuwa
from mod.youso import Youso
from mod.controller import controller

class Banmen():
    def __init__(self) -> None:
        self.own_mikoto = Mikoto(is_own=True)
        self.enemy_mikoto = Mikoto(is_own=False)
        self.maai = Utuwa(img=IMG_MAAI_AREA, is_own=True, num=10, x=WX-200, y=310)
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
