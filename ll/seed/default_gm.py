from any.game_master import GameMaster
from model.board import Board
from model.player import Player, OBSERVER
from view.board_view import BoardView
from view.draw_view import DrawView

def _make_board() -> Board:
    players: list[Player] = [
        Player.new_man(name="Johann", color="crimson"),
        Player.new_man(name="Seiji", color="darkgreen"),
        Player.new_man(name="William", color="purple"),
        Player.new_man(name="Gastone", color="gold")]
    return Board.new_board(players=players)

board = _make_board()
gm = GameMaster(board=board)
view = BoardView(board=board, subject=OBSERVER, listener=gm)
print("view", view.__class__)
print("view.listener", view.listener.__class__)
# _board_view = BoardView(board=board, subject=OBSERVER, listener=gm)
# view = DrawView(view=_board_view)
gm.view = view
print("gm.view", gm.view.__class__)
