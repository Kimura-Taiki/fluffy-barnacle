def coord() -> list[int]:
    return [0, 0]

cz = [coord(), coord(), coord(), coord()]
print(cz)
cz[2][1] = 99
print(cz)
