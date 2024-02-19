class A:
    def __init__(self) -> None:
        self.x, self.y = 0, 0

    def hoge(self) -> None:
        ...

    def call(self) -> None:
        print(self.hoge)
        print(type(self.hoge))

A().call()
