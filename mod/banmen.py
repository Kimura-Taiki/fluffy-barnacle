from mod.card import Card

class Banmen():
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def taba(self, hs: int, cr: int) -> list[Card]:
        return [card for card in self.cards if card.hoyuusya == hs and cr in card.ryouiki]