a = [0.1]*10
print(a)
exit()

from typing import Callable, Generator

class Huda():
    def __init__(self, x: int, y: int, hovered: Callable[["Huda"], Callable[[], None]]) -> None:
        self.x, self.y = x, y
        self.hovered: Callable[..., None] = hovered(self)

    @classmethod
    def made_by_files(cls, strs: list[str]) -> list["Huda"]:
        j = len(strs)
        return [Huda(x=i, y=i**2, hovered=_generate_hovered_tehuda) for i, v in enumerate(strs)]

def _generate_hovered_tehuda(huda: Huda) -> Callable[..., None]:
    def method() -> None:
        print(f"座標は({huda.x},{huda.y})です")
    return method

hudas = Huda.made_by_files(strs=["りんご", "Gorilla", "喇叭", "パセリ"])
print(hudas, hudas[3].hovered())



'''
from functools import partial

class Huda:
    def __init__(self, img, angle, scale, x, y, gen):
        self.img = img
        self.angle = angle
        self.scale = scale
        self.x = x
        self.y = y
        self.gen = gen(self)

# ジェネレータ関数の例
def g(huda_instance):
    def custom_method():
        print(f"Custom method called for Huda with image: {huda_instance.img}")
    return custom_method

# 使用例
def HAND_ANGLE(i, j):
    # 仮の実装
    return i + j

def HAND_X(i, j):
    # 仮の実装
    return i + j

def HAND_Y(i, j):
    # 仮の実装
    return i + j

# リスト内包表記で Huda インスタンスを生成
huda_instances = [Huda(img=f"example_image{i}{j}.png", angle=HAND_ANGLE(i, j), scale=0.6, x=HAND_X(i, j), y=HAND_Y(i, j), gen=partial(g)) for i in range(5) for j in range(5)]

# カスタムメソッドを呼び出す例
for huda_instance in huda_instances:
    huda_instance.gen()  # この時点で自身のインスタンスが渡されます

Hudaクラスのインスタンスに、クラス外部から定義できるインスタンスメソッドの様な挙動を示すhovered属性を作ります。
例：huda.hovered()と書くとhoveredに指定された命令がhudaインスタンスを唯一の引数として起動する。
この時、以下の２つの実装が思い付いたのですがそれぞれの利点難点を述べつつどちらが良さそうか教えてください。


1️⃣：生の命令をHudaインスタンス生成時に送り、hoveredは生の命令を部分適用したpartial型を抱える。
from typing import Callable
from functools import partial

class Huda():
    def __init__(self, x: int, y: int, hovered: Callable[..., None]) -> None:
        self.x, self.y = x, y
        self.hovered: Callable[..., None] = partial(hovered, huda=self)

    @classmethod
    def made_by_files(cls, strs: list[str]) -> list["Huda"]:
        j = len(strs)
        return [Huda(x=i, y=i**2, hovered=partial(_nama_hovered_tehuda)) for i, v in enumerate(strs)]

def _nama_hovered_tehuda(huda: Huda) -> None:
    print(f"座標は({huda.x},{huda.y})です")

hudas = Huda.made_by_files(strs=["りんご", "Gorilla", "喇叭", "パセリ"])



2️⃣：ジェネレーターをインスタンス生成時に送り、hoveredはジェネレーターから生成されたfunction型を抱える。
from typing import Callable

class Huda():
    def __init__(self, x: int, y: int, hovered: Callable[..., None]) -> None:
        self.x, self.y = x, y
        self.hovered: Callable[..., None] = hovered(self)

    @classmethod
    def made_by_files(cls, strs: list[str]) -> list["Huda"]:
        j = len(strs)
        return [Huda(x=i, y=i**2, hovered=_generate_hovered_tehuda) for i, v in enumerate(strs)]

def _generate_hovered_tehuda(huda: Huda) -> Callable[..., None]:
    def method() -> None:
        print(f"座標は({huda.x},{huda.y})です")
    return method

hudas = Huda.made_by_files(strs=["りんご", "Gorilla", "喇叭", "パセリ"])
'''