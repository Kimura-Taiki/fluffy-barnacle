from mod.const import UC_ZYOGAI, UC_SYUUTYUU, UC_ISYUKU
from mod.delivery import Delivery

def syuutyuu(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=1)

def full_syuutyuu(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_SYUUTYUU, kazu=2)

def reduce_syuutyuu(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_SYUUTYUU, to_code=UC_ZYOGAI, kazu=2)

def isyuku(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_code=UC_ZYOGAI, to_code=UC_ISYUKU, kazu=1)

def isyuku_mine(delivery: Delivery, hoyuusya: int) -> None:
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_code=UC_ZYOGAI, to_mine=True, to_code=UC_ISYUKU, kazu=1)
