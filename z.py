from mod.card import *

# 書き方１
int_di: Callable[[int], SuuziDI] = lambda i: lambda delivery, hoyuusya: i
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: lambda delivery, hoyuusya: [j == i for j in range(11)]
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: lambda delivery, hoyuusya: [i <= k <= j for k in range(11)]

# 書き方２
int_di: Callable[[int], SuuziDI] = lambda i: partial(lambda delivery, hoyuusya, teisuu: teisuu, teisuu=i)
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: partial(lambda delivery, hoyuusya, teisuu: [j == teisuu for j in range(11)], teisuu=i)
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: partial(lambda delivery, hoyuusya, minsuu, maxsuu: [minsuu <= k and k <= maxsuu for k in range(11)], minsuu=i, maxsuu=j)
