from functools import partial

class Low:
    def __init__(self, x) -> None:
        self.x = x

class High:
    def __init__(self, low) -> None:
        self.low = low

def low_mes(low):
    print(low.x)

def high_mes(high):
    print(high.low.x)

low1 = Low(10)
low2 = Low(20)
high = High(low1)
hlm = partial(low_mes, high.low)
hlm = partial(high_mes, high)
hlm = partial(low_mes, low1)
hlm()
low1.x = 55; hlm()
high.low = low2; hlm()
low1 = Low(99); hlm()