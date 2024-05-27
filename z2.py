import pygame
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

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Love Letter")

# カードクラス
class Card:
    def __init__(self, name: str, image: pygame.Surface):
        self.name = name
        self.effect = CARD_EFFECTS[name]
        self.image = image

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
                image = pygame.transform.rotozoom(pygame.image.load(f'images/{name.lower()}.png'), 0.0, 0.3)  # 画像のパス
                self.cards.append(Card(name, image))

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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw_screen()
            pygame.display.flip()

    def draw_screen(self):
        screen.fill((0, 128, 0))  # 背景色
        for i, player in enumerate(self.players):
            self.draw_player_hand(i, player)
        # その他の描画...

    def draw_player_hand(self, i: int, player: Player):
        for j, card in enumerate(player.hand):
            x = 100 + j * 120 + i * 150
            y = 300 if player == self.players[self.current_player_idx] else 100
            screen.blit(card.image, (x, y))

    def handle_click(self, pos):
        player = self.players[self.current_player_idx]
        for i, card in enumerate(player.hand):
            x = 100 + i * 120 + i * 150
            y = 300
            card_rect = pygame.Rect(x, y, card.image.get_width(), card.image.get_height())
            if card_rect.collidepoint(pos):
                self.play_card(player, card)
                break

    def play_card(self, player: Player, card: Card):
        print(f"{player.name} plays {card}")
        player.discard_card(card.name)
        self.resolve_card_effect(player, card)
        self.next_player()

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

# ゲームを開始する
players = [Player("Alice"), Player("Bob"), Player("Charlie"), Player("Diana")]
game = LoveLetterGame(players)
game.play()

pygame.quit()
