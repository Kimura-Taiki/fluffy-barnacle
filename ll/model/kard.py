from pygame import Surface
from typing import Protocol, runtime_checkable, Callable, Any

@runtime_checkable
class Kard(Protocol):
    png_file: str
    picture: Callable[[], Surface]
    name: str
    rank: int
    use_func: Callable[[Any, Any], None]
    '''
    use_func(Board, Player) -> None

    カードを使用した際に起動する命令です。
    第１引数にBoard,第２引数にPlayerを代入してください。
    '''