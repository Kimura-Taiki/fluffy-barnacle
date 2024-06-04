from any.func import make_progress_funcs
from model.ui_element import UIElement
from ptc.transition import Transition

from ptc.view import View
class MovesView():
    def __init__(self, view: View, transitions: list[Transition]) -> None:
        self.in_progress, self._complete = make_progress_funcs()
        self.view = view
        self.transitions = transitions
        self.ui_element = UIElement(mousedown=self._complete)

    def rearrange(self) -> None:
        ...

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def draw(self) -> None:
        self.view.draw()
        for transition in self.transitions:
            transition.draw()

    def elapse(self) -> None:
        for transition in self.transitions:
            transition.elapse()
        self.transitions = [ts for ts in self.transitions if ts.in_progress()]
        if not self.transitions:
            self._complete()
