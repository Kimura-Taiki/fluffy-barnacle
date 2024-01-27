from mod.ol.main_phase import MainPhase
mp = MainPhase()
mp.close()
if 1: print(1)
if 0: print(0)
if -1: print(-1)

print("ZZZ")


class Banmen():
    def __init__(self) -> None:
        self.listeners: list[Listener] = [item for sublist in [i.tenko() for i in li] for item in sublist]
        for listener in self.listeners:
            listener.delivery = self
        self.tabas: list[Taba] = []
        for listener in self.listeners:
            if isinstance(listener, Taba):
                self.tabas.append(listener)
