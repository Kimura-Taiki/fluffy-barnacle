def call(b: bool) -> bool:
    print("call")
    return b

def dif(c1: bool, c2: bool) -> int:
    print(1 if call(c1) else 2 if call(c2) else 3)

dif(True, True)
dif(True, False)
dif(False, True)
dif(False, False)