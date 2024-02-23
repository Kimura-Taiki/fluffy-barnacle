#                 20                  40                  60                 79
from mod.const import IMG_SYUUTYUU_AREA, OBAL_SYUUTYUU
from mod.classes import partial
from mod.mkt.utuwa import Utuwa
from mod.kd.action_circle import mousedown, active, mouseup

def syuutyuu_utuwa(hoyuusya: int, osame: int, x: int, y: int) -> Utuwa:
    return Utuwa(
        img=IMG_SYUUTYUU_AREA, hoyuusya=hoyuusya, osame=osame, x=x, y=y, max=2,
        mousedown=partial(mousedown, mode=OBAL_SYUUTYUU),
        active=partial(active, mode=OBAL_SYUUTYUU),
        mouseup=partial(mouseup, mode=OBAL_SYUUTYUU))
