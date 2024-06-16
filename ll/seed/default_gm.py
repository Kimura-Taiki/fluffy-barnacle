from any.game_master import GameMaster
from model.board import Board
from model.player import Player
from seed.default_deck import inject_deck
from seed.default_router import router
from view.board_view import BoardView

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

board.setups_async = router.setups_async
board.turn_starts_async = router.turn_starts_async
board.draw_kards_async = router.draw_kards_async
board.use_kards_async = router.use_kards_async
board.win_by_strengths_async = router.win_by_strengths_async
board.win_by_survivals_async = router.win_by_survivals_async

board.drawn_funcs_async = router.drawn_funcs_async
board.diskard_funcs_async = router.diskard_funcs_async

gm.board.setups_async()
