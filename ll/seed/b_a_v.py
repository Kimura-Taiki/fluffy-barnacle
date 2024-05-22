from pygame import Color

from mod.board import Board
from mod.kard import Kard, EMPTY_KARD
from mod.board_view import BoardView
from mod.man_player import ManPlayer
from ptc.player import Player, OBSERVER

def _make_board() -> Board:
    players: list[Player] = [
        ManPlayer(name="Johann", color="crimson", log=[]),
        ManPlayer(name="Seiji", color="darkgreen", log=[]),
        ManPlayer(name="William", color="purple", log=[]),
        ManPlayer(name="Gastone", color="gold", log=[])]
    return Board(players=players)

# class Observer():
#     def __init__(self) -> None:
#         self.name = "(Observer)"
#         self.color = Color("white")
#         self.hand = EMPTY_KARD
#         self.log: list[Kard] = []

board = _make_board()
# view = BoardView(board=board, subject=board.players[0])
view = BoardView(board=board, subject=OBSERVER)
