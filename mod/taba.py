class Huda():
    def __init__(self, name: str) -> None:
        self.name = name

class Taba(list[Huda]):
    def __init__(self, data: list[Huda]=[]) -> None:
        super().__init__(data)
        self.other_params: list[int] = []

    def method(self) -> None:
        for huda in self:
            print(huda.name)
        pass

taba = Taba(data=[Huda("Alpha"), Huda("Beta")])

taba.method()
