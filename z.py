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
