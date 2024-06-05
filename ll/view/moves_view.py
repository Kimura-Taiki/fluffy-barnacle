from ptc.transition import Transition
from view.progress_helper import ProgressHelper

from ptc.view import View
class MovesView():
    def __init__(self, view: View, transitions: list[Transition]) -> None:
        self._ratio, self.in_progress, self._complete, _, self.get_hover, _\
            = ProgressHelper(seconds=0.0).provide_progress_funcs()
        self.view = view
        self.transitions = transitions

    def rearrange(self) -> None:
        ...

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
