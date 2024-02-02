from mod.const import compatible_with, REQ_OUKA
from mod.req.request import Request

class ReqOuka():
    request_code: int = REQ_OUKA

    def __init__(self, hoyuusya: int, is_mine: bool, utuwa_code: int) -> None:
        self.hoyuusya = hoyuusya
        self.is_mine = is_mine
        self.utuwa_code = utuwa_code

compatible_with(obj=ReqOuka(0, True, 0), protocol=Request)
