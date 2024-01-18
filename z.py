# 手札, 切り札, 捨札&伏札, 山札

# 集中, オーラ, フレア, ライフ
# (未使用&追加&除外)

from typing import Callable
from functools import partial

func: Callable[[int, int], float] = lambda i, j: (i**2+j**2)**0.5

j5func = partial(func, j=5)
print(j5func(12))