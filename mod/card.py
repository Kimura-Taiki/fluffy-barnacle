from mod.zyouhou import Zyouhou

class Card():
    def __init__(self, zh: Zyouhou) -> None:
        self.zh = zh