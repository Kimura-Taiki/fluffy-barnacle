def p(i: int) -> None:
    print(i)

[x if (x := p(i)) else False for i in range(5)]