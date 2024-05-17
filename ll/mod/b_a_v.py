from mod.board import Board
from mod.board_view import BoardView
from mod.man_player import ManPlayer
from ptc.player import Player

def _make_board() -> Board:
    players: list[Player] = [ManPlayer(name="Alpha", color="red"), ManPlayer(name="Bravo", color="yellow"),
               ManPlayer(name="Charly", color="green"), ManPlayer(name="Delta", color="blue")]
    return Board(players=players)

board = _make_board()
view = BoardView(board=board)