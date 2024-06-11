from any.func import enforce
from any.screen import screen
from model.board import Board
from model.player import Player
from ptc.bridge import Bridge
from view.board_view import BoardView
from view.transition.linear_transition import LinearTransition
from view.moves_view import MovesView
from view.player_square import PlayerSquare
from view.player_select_view import PlayerSelectView

class SyougunEffect():
    def __init__(self) -> None:
        pass

    def use_func(self, board: Board, player: Player) -> None:
        

def exchange_kards(self, p1: Player, p2: Player) -> None:
    """二人のプレイヤー間でカードを交換する処理を行います。"""
    if p1.protected or p2.protected:
        from model.deck import KARD_SYOUGUN
        self.guard_async(KARD_SYOUGUN)
        return
    self.exchange_kards_async(p1, p2)
    p1.hands, p2.hands = p2.hands, p1.hands


def _use_syougun(self) -> None:
    print("カード「将軍」を使ったよ")
    self.bridge.whileloop(new_view=(psv := PlayerSelectView(
        bridge=self.bridge,
        exclude=self.bridge.board.turn_player,
    )))
    self.bridge.board.exchange_kards(
        p1=self.bridge.board.turn_player,
        p2=psv.selected_player
    )
#       10        20        30        40        50        60        70       79
    # print(psv.selected_player)
    # raise EOFError("良し！")

class ExchangeKardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge
        self.board_view = enforce(bridge.view, BoardView)
        self.img_back = self.board_view.deck_square.img_back

    def action(self, p1: Player, p2: Player) -> None:
        p1_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=p1,
        )
        p2_v2 = PlayerSquare.search_v2_by_player(
            squares=self.board_view.squares,
            player=p2
        )
        self.bridge.whileloop(new_view=MovesView(
            view=self.bridge.view,
            transitions=[
                LinearTransition(
                    img_actor=self.img_back,
                    from_v2=f,
                    to_v2=t,
                    canvas=screen
                )
                for f, t in [(p1_v2, p2_v2), (p2_v2, p1_v2)]
            ]
        ))
