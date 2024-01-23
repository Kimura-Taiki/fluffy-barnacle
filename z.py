from functools import partial, partialmethod

class Cls:
    def func(self) -> None:
        print("Clsの命令です")

c1 = Cls()
c2 = Cls()
c1.func()
c2.func()
def xyz() -> None:
    print("XYZ-ドラゴン・キャノン")
c1.func = partial(xyz)
c1.func()
c2.func()
