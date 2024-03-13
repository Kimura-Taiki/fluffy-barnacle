#                 20                  40                  60                 79
from random import shuffle

from mod.const import TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA, USAGE_DEPLOYED,\
    enforce
from mod.classes import Huda, Taba, Delivery
from mod.card.temp_koudou import TempKoudou, auto_di

def _saikousei_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    taba1, taba2, taba3 = [enforce(delivery.taba_target(hoyuusya=hoyuusya,
        is_mine=True, taba_code=taba_code), Taba) for taba_code in
        [TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA]]
    moto = list(taba1)+list(taba2)+[
        huda for huda in taba3 if huda.usage!= USAGE_DEPLOYED]
    shuffle(moto)
    return moto

def saikousei(delivery: Delivery, hoyuusya: int) -> None:
    for huda in _saikousei_hudas(delivery=delivery, hoyuusya=hoyuusya):
        delivery.send_huda_to_ryouiki(huda=huda, is_mine=True, taba_code=
                                      TC_YAMAHUDA)

saikousei_card = TempKoudou(name="再構成", cond=auto_di, kouka=saikousei)