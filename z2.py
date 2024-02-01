class _Hoge:
    x: int
    y: int

def length(hoge: _Hoge) -> float:
    gg = float((hoge.x**2+hoge.y**2)**0.5)
    return gg
