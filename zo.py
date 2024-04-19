# from typing import Callable

# Do = Callable[[Board], None]

# class Card():
#     def __init__(self, name: str, do: Do) -> None:
#         self.name, self.do = name, do

# class Board():
#     def __init__(self, cards: list[Card]) -> None:
#         self.cards = cards

# def do1(board: Board) -> None:
#     print("do1です")

# def do2(board: Board) -> None:
#     print([card.name for card in board.cards])

# board = Board(cards=[Card(name="Card1", do=do1), Card(name="Card2", do=do2)])

# board.cards[0].do(board)
# board.cards[1].do(board)

# card.py
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from mod.banmen import Banmen as Board

class Card:
    def __init__(self, name: str, do: Callable[['Board'], None]) -> None:
        self.name = name
        self.do = do