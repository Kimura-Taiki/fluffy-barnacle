class Card():
    def __init__(self, name: str) -> None:
        self.name = name
    ...

class Huda():
    def __init__(self, card: Card) -> None:
        self.card = card
    ...

# def has_name(li: list[Huda], name: str) -> bool:
#     for huda in li:
#         if huda.card.name == name:
#             return True
#     return False

def has_name(li: list[Huda], name: str) -> bool:
    return any(huda.card.name == name for huda in li)
