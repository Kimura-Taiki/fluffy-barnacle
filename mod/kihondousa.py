from mod.const import UC_MAAI, UC_AURA, UC_DUST, UC_FLAIR
from mod.delivery import Delivery
from mod.popup_message import popup_message

def pass_koudou(delivery: Delivery, hoyuusya: int) -> None:
    pass

def can_zensin(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)

def zensin(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="前進します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_MAAI, to_mine=True, to_code=UC_AURA)

def can_ridatu(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_MAAI)

def ridatu(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="離脱します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_MAAI)

def can_koutai(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_MAAI)

def koutai(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="後退します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_MAAI)

def can_matoi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)

def matoi(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="纏います")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_DUST, to_mine=True, to_code=UC_AURA)

def can_yadosi(delivery: Delivery, hoyuusya: int) -> bool:
    return delivery.can_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)

def yadosi(delivery: Delivery, hoyuusya: int) -> None:
    popup_message.add(text="宿します")
    delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_AURA, to_mine=True, to_code=UC_FLAIR)
