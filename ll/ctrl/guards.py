from dataclasses import dataclass
from typing import Callable

from any.locales import lomes
from ptc.bridge import Bridge
from view.message_view import MessageView

from ptc.controller import Controller
@dataclass
class GuardsController():
    injector: Callable[[], Bridge]

    @property
    def bridge(self) -> Bridge:
        return self.injector()

    def action(self, kard_name: str) -> None:
        self.bridge.whileloop(new_view=MessageView(
            view=self.bridge.view,
            img_mes=lomes(folder="board", key="guards", kard_name=kard_name)
        ))
