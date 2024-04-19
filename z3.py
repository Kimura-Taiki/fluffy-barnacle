from z1 import Board
from z2 import Card

def do0(board: Board) -> None:
    print("Do0です")

def do1(board: Board) -> None:
    print([card.name for card in board.cards])

board = Board(cards=[Card(name="000", do=do0), Card(name="1", do=do1)])
for card in board.cards:
    card.do(board)
