from random import randrange

N = 2
K = 3

def trick(wins: list[int]) -> int:
    index = randrange(0, len(wins)) 
    wins[index] += 1
    return wins[index]

def game(player: int, win: int) -> int:
    wins = [0]*player
    tricks = 0
    while True:
        tricks += 1
        if trick(wins=wins) >= win:
            break
    return tricks

def distri(player: int, win: int, attempts: int) -> list[int]:
    li = [0]*(player*win)
    for _ in range(attempts):
        li[game(player=player, win=win)] += 1
    return li

def exp(player: int, win: int, attempts: int) -> float:
    li1 = distri(player=player, win=win, attempts=attempts)
    li2 = list(range(len(li1)))
    return sum(x*y for x, y in zip(li1, li2))/sum(li1)

for p in range(1000, 10001, 1000):
    print(f"{p}人時の勝敗確定トリック数期待値", exp(player=p, win=K, attempts=10000))