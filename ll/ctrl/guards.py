from any.locales import lomes
from model.kard import Kard
from ptc.bridge import Bridge
from view.message_view import MessageView

class GuardsController():
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    # def action(self, kard: Kard) -> None:
    #     self.bridge.whileloop(new_view=MessageView(
    #         view=self.bridge.view,
    #         img_mes=lomes(folder="kard", key="guards", kard_name=kard.name)
    #     ))
    def action(self, kard_name: str) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=lomes(folder="kard", key="guards", kard_name=kard_name)
        ))
