from any.locales import lomes
from ptc.bridge import Bridge
from view.message_view import MessageView

def guard_message(bridge: Bridge, kard_name: str) -> None:
    bridge.whileloop(new_view=MessageView(
        view=bridge.view,
        img_mes=lomes(folder="kard", key="guards", kard_name=kard_name)
    ))
