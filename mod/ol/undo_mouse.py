from functools import partial

from mod.huda import Huda
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.youso import Youso

def undo_mouseup(huda: Huda, text: str="") -> None:
    # popup_message.add(text=f"{text}'s_undo.mouseup でクリック確定したよ")
    moderator.pop()

def make_undo_youso(text: str="") -> Youso:
    return Youso(mousedown=Huda.mousedown, mouseup=partial(undo_mouseup, text=text))
