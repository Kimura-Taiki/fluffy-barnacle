from any.game_master import GameMaster
from ctrl.bright_kards import BrightKardsController
from ctrl.defeat_by_duels import DefeatByDuelsController
from ctrl.defeat_by_ministers import DefeatByMinistersController
from ctrl.diskard_himes import DiskardHimesController
from ctrl.draw_kards import DrawKardsController
from ctrl.duels import DuelsController
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.guards import GuardsController
from ctrl.protects import ProtectsController
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

view = BoardView(subject=OBSERVER, bridge=gm)
gm.view = view

board.draw_kard_async = DrawKardsController(
    bridge=gm
).action
board.turn_start_async = TurnStartsController(
    bridge=gm
).action
board.use_kard_async = BrightKardsController(
    bridge=gm
).action
board.diskard_hime_async = DiskardHimesController(
    bridge=gm
).action

board.duel_async = DuelsController(
    bridge=gm
).action
board.defeat_by_duel_async = DefeatByDuelsController(
    bridge=gm
).action
board.protect_async = ProtectsController(
    bridge=gm
).action
board.guard_async = GuardsController(
    bridge=gm
).action
board.exchange_kards_async = ExchangeKardsController(
    bridge=gm
).action
board.defeat_by_daizin_async = DefeatByMinistersController(
    bridge=gm
).action

SetupsController(bridge=gm).action()