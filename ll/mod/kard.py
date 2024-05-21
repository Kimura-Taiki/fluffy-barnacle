class Kard():
    def __init__(self, name: str, png_file: str) -> None:
        self.name = name
        self.png_file = png_file

EMPTY_KARD = Kard(name="empty", png_file="")