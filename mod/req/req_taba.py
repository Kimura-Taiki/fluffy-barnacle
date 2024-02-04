from mod.const import compatible_with, REQ_TAIOU_TABA
from mod.req.request import Request

class ReqTaba():
    request_code = REQ_TAIOU_TABA

    def __init__(self, hoyuusya: int, is_mine: bool, taba_code: int) -> None:
        self.hoyuusya = hoyuusya
        self.is_mine = is_mine
        self.taba_code = taba_code
    
compatible_with(obj=ReqTaba(0, True, 0), protocol=Request)
