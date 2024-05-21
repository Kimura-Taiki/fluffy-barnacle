from mod.board import Board
from mod.board_view import BoardView
from mod.man_player import ManPlayer
from ptc.player import Player

def _make_board() -> Board:
    players: list[Player] = [
        ManPlayer(name="you", color="crimson", log=[]),
        ManPlayer(name="Seiji", color="darkgreen", log=[]),
        ManPlayer(name="William", color="purple", log=[]),
        ManPlayer(name="Gastone", color="gold", log=[])]
    return Board(players=players)

board = _make_board()
view = BoardView(board=board, subject=board.players[0])