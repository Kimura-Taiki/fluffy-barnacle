from any.game_master import GameMaster
from ctrl.bright_kards import BrightKardsController
from ctrl.diskard_funcs import DiskardFuncsController
from ctrl.draw_kards import DrawKardsController
from ctrl.drawn_funcs import DrawnFuncsController
from ctrl.turn_starts import TurnStartsController
from ctrl.setups import SetupsController
from ctrl.win_by_strengths import WinByStrengthsController
from ctrl.win_by_survivals import WinBySurvivalsController
from model.board import Board
from model.player import Player
from seed.default_deck import inject_deck
from view.board_view import BoardView

# def _make_board() -> Board:
#     players: list[Player] = [
#         Player.new_man(name="Johann", color="crimson"),
#         Player.new_man(name="Seiji", color="darkgreen"),
#         Player.new_man(name="William", color="purple"),
#         Player.new_man(name="Gastone", color="gold")
#     ]
#     return Board.new_board(players=players)

# board = _make_board()
# gm = GameMaster(board=board)

def _make_board() -> Board:
    players: list[Player] = [
        Player.new_man(name="Johann", color="crimson"),
        Player.new_man(name="Seiji", color="darkgreen"),
        Player.new_man(name="William", color="purple"),
        Player.new_man(name="Gastone", color="gold")
    ]
    return Board(players=players)

board = _make_board()
gm = GameMaster(board=board)
view = BoardView(subject=board.players[0], bridge=gm)
gm.view = view
inject_deck(bridge=gm)

board.draw_kard_async = DrawKardsController(
    bridge=gm
).action
board.drawn_func_async = DrawnFuncsController(
    bridge=gm
).action
board.turn_start_async = TurnStartsController(
    bridge=gm
).action
board.use_kard_async = BrightKardsController(
    bridge=gm
).action
board.diskard_func_async = DiskardFuncsController(
    bridge=gm
).action
board.win_by_survival_async = WinBySurvivalsController(
    bridge=gm
).action
board.win_by_strength_async = WinByStrengthsController(
    bridge=gm
).action

# board.arrest_async = ArrestsController(
#     bridge=gm
# ).action
# board.peep_async = PeepsController(
#     bridge=gm
# ).action
# board.duel_async = DuelsController(
#     bridge=gm
# ).action
# board.defeat_by_duel_async = DefeatByDuelsController(
#     bridge=gm
# ).action
# board.protect_async = ProtectsController(
#     bridge=gm
# ).action
# board.guard_async = GuardsController(
#     bridge=gm
# ).action
# board.exchange_kards_async = ExchangeKardsController(
#     bridge=gm
# ).action
# board.defeat_by_daizin_async = DefeatByMinistersController(
#     bridge=gm
# ).action
# board.diskard_hime_async = DiskardHimesController(
#     bridge=gm
# ).action

SetupsController(bridge=gm).action()