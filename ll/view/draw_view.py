from any.screen import screen, WX, WY
from any.propagation import propagation
from any.font import MS_MINCHO_COL
from ptc.element import Element

from ptc.view import View
class DrawView():
    def __init__(self, view: View) -> None:
        self.board_view = view

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
        propagation.mouse_over()
