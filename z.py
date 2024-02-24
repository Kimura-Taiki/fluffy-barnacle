from typing import Callable, TypeVar

# クラスX
class X:
    def __init__(self, name: str) -> None:
        self.name = name
        self.f1: Callable[[X], X] = lambda x: x  # 初期値は恒等写像
        self.f2: Callable[[X], X] = lambda x: x  # 他の写像も同様に設定可能
        # ...

    def apply_f1(self) -> None:
        # f1を適用するメソッド
        result = self.f1(self)
        print(f"{self.name} applied f1, result: {result.name}")

    def apply_f2(self) -> None:
        # f2を適用するメソッド
        result = self.f2(self)
        print(f"{self.name} applied f2, result: {result.name}")
        # ...

# クラスF
class F:
    def __init__(self, name: str, f: Callable[[X], X]) -> None:
        self.name = name
        self.f = f

    def apply(self, x: X) -> X:
        # 写像を適用するメソッド
        result = self.f(x)
        print(f"{self.name} applied, result: {result.name}")
        return result

# テスト用のインスタンスを作成
x1 = X(name="X1")
x2 = X(name="X2")

# Xに写像を設定
x1.f1 = lambda x: X(name=f"f1({x.name})")
x1.f2 = lambda x: X(name=f"f2({x.name})")

# Fを作成
f1 = F(name="F1", f=lambda x: X(name=f"F1({x.name})"))
f2 = F(name="F2", f=lambda x: X(name=f"F2({x.name})"))

# FをXに適用
result1 = f1.apply(x1)
result2 = f2.apply(x2)

# Xに保存された写像を適用
x1.apply_f1()
x1.apply_f2()
