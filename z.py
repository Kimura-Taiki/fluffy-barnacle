def coord3(x: int, y: int, z: int) -> None:
    print(f"Coord3 = ({x}, {y}, {z})")

class Kws:
    def __init__(self, **kwargs) -> None:
        coord3(**kwargs)
        print("print = ", kwargs)
        self.kwargs = kwargs

Kws(x=10, y=35, z=99)