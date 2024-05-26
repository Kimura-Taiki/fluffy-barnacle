from pygame import Surface, Vector2 as V2
from typing import Callable

from any.font import MS_MINCHO_COL
from any.screen import screen, WX, WY
from any.timer_functions import frames
from ptc.element import Element

from ptc.view import View
# from ptc.element import Element
class DrawView():
    def __init__(self, view: View, img_back: Surface, from_v2: V2, to_v2: V2, callback: Callable[[], None]) -> None:
        self.board_view = view
        self.img_back = img_back
        self.from_v2 = from_v2
        self.to_v2 = to_v2
        self.callback = callback
        self.frames = frames()

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> Element | None:
        return None

    def draw(self) -> None:
        self.board_view.draw()
        screen.blit(
            source=MS_MINCHO_COL("in drawing...", 64, "black"),
            dest=(WX/2-112, WY/2-32)
        )
        screen.blit(
            source=self.img_back,
            dest=self.from_v2.lerp(self.to_v2, (frames()-self.frames)/180)-V2(self.img_back.get_size())/2
        )
