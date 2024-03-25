def iff(x: bool, y: bool) -> None:
    print("Alpha" if x else "Beta" if y else "Gamma")

iff(False, False)
iff(False, True)
iff(True, False)
iff(True, True)