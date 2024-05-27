import random
from typing import List

# 定数
CARD_NAMES = [
    "Guard", "Priest", "Baron", "Handmaid", "Prince", "King", "Countess", "Princess"
]
CARD_EFFECTS = {
    "Guard": "Guess a player's hand",
    "Priest": "Look at a player's hand",
    "Baron": "Compare hands, lower hand is out",
    "Handmaid": "Protection until your next turn",
    "Prince": "One player discards their hand",
    "King": "Trade hands with another player",
    "Countess": "Must discard if caught with King or Prince",
    "Princess": "Lose if you discard this card"
}
CARD_COUNTS = {
    "Guard": 5,
    "Priest": 2,
    "Baron": 2,
    "Handmaid": 2,
    "Prince": 2,
    "King": 1,
    "Countess": 1,
    "Princess": 1
}

# カードクラス
class Card:
    def __init__(self, name: str):
        self.name = name
        self.effect = CARD_EFFECTS[name]

    def __repr__(self):
        return f"{self.name}({self.effect})"

# プレイヤークラス
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.protected = False
        self.out = False

    def draw_card(self, card: Card):
        self.hand.append(card)

    def discard_card(self, card_name: str):
        self.hand = [card for card in self.hand if card.name != card_name]

    def __repr__(self):
        return f"Player({self.name}, Hand: {self.hand}, Protected: {self.protected})"

# デッキクラス
class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.build_deck()
        self.shuffle()

    def build_deck(self):
        for name, count in CARD_COUNTS.items():
            for _ in range(count):
                self.cards.append(Card(name))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop() if self.cards else None

# ゲームクラス
class LoveLetterGame:
    def __init__(self, players: List[Player]):
        self.players = players
        self.deck = Deck()
        self.current_player_idx = 0

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def play(self):
        for player in self.players:
            player.draw_card(self.deck.draw())
        while len(self.deck.cards) > 0 and not self.is_game_over():
            player = self.players[self.current_player_idx]
            if not player.out:
                print(f"{player.name}'s turn")
                for ppp in [ppp for ppp in self.players if not ppp.out]:
                    print(f"    {ppp}")
                self.player_turn(player)
            self.next_player()
        self.determine_winner()

    def player_turn(self, player: Player):
        if player.protected:
            player.protected = False

        drawn_card = self.deck.draw()
        player.draw_card(drawn_card)
        print(f"{player.name} drew a {drawn_card}")

        # カードを捨てて効果を発動する（簡易版）
        played_card = player.hand.pop(0)
        print(f"{player.name} plays {played_card}")
        self.resolve_card_effect(player, played_card)

    def resolve_card_effect(self, player: Player, card: Card):
        # 簡易版：カード効果を解決する（実際のルールに従って拡張可能）
        if card.name == "Guard":
            target = self.choose_target(player)
            guess = self.guess_card(player)
            if any(c.name == guess for c in target.hand):
                target.out = True
                print(f"{target.name} is out!")
        elif card.name == "Priest":
            target = self.choose_target(player)
            print(f"{target.name}'s hand: {target.hand}")
        elif card.name == "Baron":
            target = self.choose_target(player)
            if target.hand[0].name != player.hand[0].name:
                loser = player if target.hand[0].name > player.hand[0].name else target
                loser.out = True
                print(f"{loser.name} is out!")
        elif card.name == "Handmaid":
            player.protected = True
        elif card.name == "Prince":
            target = self.choose_target(player)
            target.discard_card(target.hand[0].name)
            target.draw_card(self.deck.draw())
        elif card.name == "King":
            target = self.choose_target(player)
            player.hand, target.hand = target.hand, player.hand
        elif card.name == "Countess":
            pass
        elif card.name == "Princess":
            player.out = True
            print(f"{player.name} is out!")

    def choose_target(self, player: Player) -> Player:
        # 簡易版：最初の有効なターゲットを選択する
        for p in self.players:
            if p != player and not p.out and not p.protected:
                return p
        return player

    def guess_card(self, player: Player) -> str:
        # 簡易版：常に"Princess"を推測する
        return "Princess"

    def is_game_over(self) -> bool:
        return sum(1 for p in self.players if not p.out) <= 1

    def determine_winner(self):
        active_players = [p for p in self.players if not p.out]
        if len(active_players) == 1:
            print(f"The winner is {active_players[0].name}")
        else:
            winner = max(active_players, key=lambda p: p.hand[0].name)
            print(f"The winner is {winner.name}")

# ゲームを開始する
players = [Player("Alice"), Player("Bob"), Player("Charlie"), Player("Diana")]
game = LoveLetterGame(players)
game.play()
