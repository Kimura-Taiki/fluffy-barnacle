from mod.board import Board
from mod.man_player import ManPlayer
from mod.board_view import BoardView
from mod.game_master import GameMaster
from ptc.player import Player, OBSERVER

def _make_board() -> Board:
    players: list[Player] = [
        ManPlayer(name="Johann", color="crimson", log=[]),
        ManPlayer(name="Seiji", color="darkgreen", log=[]),
        ManPlayer(name="William", color="purple", log=[]),
        ManPlayer(name="Gastone", color="gold", log=[])]
    return Board(players=players)

board = _make_board()

view = BoardView(board=board, subject=OBSERVER)

gm = GameMaster(board=board, view=view)