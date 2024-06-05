from typing import Callable

from any.timer_functions import make_ratio_func
from model.ui_element import UIElement

class ProgressHelper:
    '''
    in_progressを中心としたメソッド群を提供します。

    seconds引数に0.0を入れた場合、ratio_funcは常に0.0を返します。
    '''
    def __init__(self, seconds: float) -> None:
        self.ratio_func = make_ratio_func(seconds=seconds) if seconds else lambda : 0.0
        self.ui_element = UIElement(mousedown=self.complete)
        self._in_progress = True

    def in_progress(self) -> bool:
        return (self.ratio_func() < 1) and self._in_progress

    def complete(self) -> None:
        self._in_progress = False

    def get_hover(self) -> UIElement | None:
        return self.ui_element

    def elapse(self) -> None:
        ...

    def provide_progress_funcs(self) -> tuple[
        Callable[[], float], Callable[[], bool], Callable[[], None],
        UIElement, Callable[[], UIElement | None], Callable[[], None]
    ]:
        '''
        ratio関数, in_progress関数, complete命令, ui_element属性, get_hover関数, elapse命令の
        メソッド六種を一括して供給します。
        不要なメソッドの項目には「_」を指定してください。戻り値を6つ全て取らないとエラーです。
        '''
        return self.ratio_func, self.in_progress, self.complete, self.ui_element, self.get_hover, self.elapse
