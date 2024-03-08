#                 20                  40                  60                 79
from mod.const import UC_DUST
from mod.delivery import Delivery

def yazirusi(delivery: Delivery, hoyuusya: int, from_mine: bool=False,
from_code: int=UC_DUST, to_mine: bool=False, to_code: int=UC_DUST,
kazu: int=1) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=from_mine,
        from_code=from_code, to_mine=to_mine, to_code=to_code, kazu=kazu)
