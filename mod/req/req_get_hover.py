from mod.const import compatible_with, REQ_GET_HOVER
from mod.req.request import Request

class ReqGetHover():
    request_code: int = REQ_GET_HOVER

compatible_with(obj=ReqGetHover(), protocol=Request)
