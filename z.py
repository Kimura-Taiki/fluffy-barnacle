from copy import copy

class Moto:
    def __init__(self, w: str, x: int, y: int) -> None:
        self.w, self.x, self.y = w, x, y

    def mes(self) -> None:
        print(f"{self.w}は({self.x}, {self.y})です")

# class Sue(Moto):
#     def __init__(self, base: Moto, z: int) -> None:
#         self = copy(base)
#         self.z = z

#     def mes(self) -> None:
#         print(f"{self.x,}, {self.y}, {self.z})")

class Sue(Moto):
    def __init__(self, base: Moto, w: str, z: int) -> None:
        # ベースのMotoインスタンスから全属性を取得
        base_attributes = vars(base)

        # Sueクラスを初期化
        for key, value in base_attributes.items():
            setattr(self, key, value)

        self.w = w
        self.z = z

    def mes(self) -> None:
        print(f"{self.w}は({self.x}, {self.y}, {self.z})です")

d2 = Moto("Moto", 3, 4)
d2.mes()

d3 = Sue(d2, "Sue", 5)
d3.mes()