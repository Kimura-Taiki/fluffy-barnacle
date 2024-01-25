from dataclasses import dataclass
from typing import NamedTuple

from typing import NamedTuple

class Signal(NamedTuple):
    code: int = 0
    text: str = ""  # 初期値を追加

# 初期値を持つ Signal インスタンスを作成
s = Signal(text="GGG")

# 結果を表示
print(s)

exit("GGG")
from typing import List

# Mediator インターフェース
class Mediator:
    def notify(self, sender: 'Colleague', message: str) -> None:
        pass

# Colleague インターフェース
class Colleague:
    def __init__(self, mediator: Mediator) -> None:
        self.mediator = mediator

    def send(self, message: str) -> None:
        pass

    def receive(self, message: str) -> None:
        pass

# 具体的な Mediator クラス
class ConcreteMediator(Mediator):
    def __init__(self) -> None:
        self.colleagues: List[Colleague] = []

    def add_colleague(self, colleague: Colleague) -> None:
        self.colleagues.append(colleague)

    def notify(self, sender: Colleague, message: str) -> None:
        for colleague in self.colleagues:
            if colleague != sender:
                colleague.receive(message)

# 具体的な Colleague クラス
class ConcreteColleague(Colleague):
    def send(self, message: str) -> None:
        print(f"Colleague sends: {message}")
        self.mediator.notify(self, message)

    def receive(self, message: str) -> None:
        print(f"Colleague receives: {message}")

# メイン部分
mediator = ConcreteMediator()

colleague1 = ConcreteColleague(mediator)
colleague2 = ConcreteColleague(mediator)

mediator.add_colleague(colleague1)
mediator.add_colleague(colleague2)

colleague1.send("Hello from Colleague 1!")
colleague2.send("Hi from Colleague 2!")
exit()

class Listener():
    def __init__(self, name: str, listeners: list['Listener'] = []) -> None:
        self.list: list['Listener'] = []
        for listener in listeners:
            listener.list.append(self)
        self.name = name

    def receive_message(self, message: str) -> None:
        print(f"{self.name}が「{message}」を受信したよ。")

    def send_message(self, message: str) -> None:
        print(f"{self.name}が「{message}」を送信したよ。")
        self._send_message(message=message)

    def _send_message(self, message: str) -> None:
        for listener in self.list:
            listener.receive_message(message=message)
            listener._send_message(message=message)


t71 = Listener(name="後三条天皇")
t70 = Listener(name="後冷泉天皇")
t69 = Listener(name="後朱雀天皇", listeners=[t71, t70])
t68 = Listener(name="後一条天皇")
t67 = Listener(name="三条天皇")
t66 = Listener(name="一条天皇", listeners=[t69, t68])
t65 = Listener(name="花山天皇")
t64 = Listener(name="円融天皇", listeners=[t66])
t63 = Listener(name="冷泉天皇", listeners=[t67, t65])
t62 = Listener(name="村山天皇", listeners=[t64, t63])
t61 = Listener(name="朱雀天皇")
t61 = Listener(name="醍醐天皇", listeners=[t62, t61])

t71.send_message(message="御堂家の時代")
