from nf.nf_code import NFC_EXIT
from ptc.notification import Notification

class NfExit():
    code: int = NFC_EXIT

    def __init__(self, mes: str="終了コードです") -> None:
        self.message = mes