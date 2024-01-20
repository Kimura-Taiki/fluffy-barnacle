from typing import Protocol

class Delivery(Protocol):
    def send_huda_to_ryouiki(self, huda: Huda, is_mine: bool, taba_code: int) -> None:
        ...
    
    def send_ouka_to_ryouiki(self, ryouiki: Ryouiki, is_mine: bool, ryouiki_code: int, count: int) -> None:
        ...