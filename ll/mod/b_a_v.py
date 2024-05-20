from mod.board import Board
from mod.board_view import BoardView
from mod.man_player import ManPlayer
from ptc.player import Player

def _make_board() -> Board:
    players: list[Player] = [ManPlayer(name="you", color="crimson"), ManPlayer(name="Seiji", color="darkgreen"),
               ManPlayer(name="William", color="purple"), ManPlayer(name="Gastone", color="gold")]
    return Board(players=players)

board = _make_board()
view = BoardView(board=board, subject=board.players[0])