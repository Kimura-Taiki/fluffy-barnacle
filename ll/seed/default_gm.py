from any.game_master import GameMaster
from ctrl.bright_kards import BrightKardsController
from ctrl.defeat_by_ministers import DefeatsByMinistersController
from ctrl.draw_kards import DrawKardsController
from ctrl.diskard_himes import DiskardHimesController
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.turn_starts import TurnStartsController
from ctrl.setups import SetupsController
from model.board import Board
from model.player import Player, OBSERVER
from view.board_view import BoardView

def _make_board() -> Board:
    players: list[Player] = [
        Player.new_man(name="Johann", color="crimson"),
        Player.new_man(name="Seiji", color="darkgreen"),
        Player.new_man(name="William", color="purple"),
        Player.new_man(name="Gastone", color="gold")
    ]
    return Board.new_board(players=players)

board = _make_board()
gm = GameMaster(board=board)

board.defeat_by_daizin_async = DefeatsByMinistersController(
    bridge=gm
).action
board.diskard_hime_async = DiskardHimesController(
    bridge=gm
).action
board.use_kard_async = BrightKardsController(
    bridge=gm
).action
board.turn_start_async = TurnStartsController(
    bridge=gm
).action

view = BoardView(subject=OBSERVER, bridge=gm)
gm.view = view

board.exchange_kards_async = ExchangeKardsController(
    bridge=gm
).action
board.draw_kard_async = DrawKardsController(
    bridge=gm
).action

SetupsController(bridge=gm).action()