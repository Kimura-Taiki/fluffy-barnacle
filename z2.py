from typing import Callable, Any

Do = Callable[[Any], None]

class Card:
    def __init__(self, name: str, do: Do) -> None:
        self.name, self.do = name, do