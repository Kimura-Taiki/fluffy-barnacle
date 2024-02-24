#                 20                  40                  60                 79
from typing import Any

from mod.popup_message import popup_message

def maai_text(bool_list: list[bool]) -> str:
    bool_list.append(False)
    text = ""
    num = -1
    chain = False
    for i, b in enumerate(bool_list):
        if b:
            if not chain:
                num, chain = i, True
        else:
            if chain:
                if i == num+1:
                    text, chain = text+","+str(num), False
                else:
                    text, chain = text+","+str(num)+"-"+str(i-1), False
    return text[1:]

def is_meet_conditions(checks: list[tuple[bool, str]], popup: bool=False) -> bool:
    for condition, message in checks:
        if condition:
            if popup:
                popup_message.add(message)
            return False
    return True
