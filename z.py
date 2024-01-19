# 手札, 切り札, 捨札&伏札, 山札

# 集中, オーラ, フレア, ライフ
# (未使用&追加&除外)

class Youso():
    def __init__(self, **kwargs) -> None:
        self.x: int | float = kwargs.get('x', 0)
        self.y: int | float = kwargs.get('y', 0)
        # その他kwargs代入

class Youso():
    def __init__(self, x: int | float=0, y: int | float=0, **kwargs) -> None:
        self.x = x
        self.y = y
        # その他kwargs代入
