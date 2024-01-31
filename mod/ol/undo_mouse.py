from functools import partial

from mod.huda import Huda
from mod.popup_message import popup_message
from mod.controller import controller
from mod.moderator import moderator
from mod.youso import Youso

def undo_mousedown(huda: Huda, text: str="") -> None:
    popup_message.add(text=f"{text}.mousedown でクリックしたよ")
    controller.active = huda

def undo_mouseup(huda: Huda) -> None:
    moderator.pop()

def make_gray_youso(text: str="") -> Youso:
    return Youso(mousedown=partial(undo_mousedown, text=text), mouseup=undo_mouseup)
