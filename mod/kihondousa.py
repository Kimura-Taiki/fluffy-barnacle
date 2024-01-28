from mod.const import UC_MAAI, UC_AURA
from mod.delivery import Delivery
from mod.popup_message import popup_message

def zensin(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="前進します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)
    
