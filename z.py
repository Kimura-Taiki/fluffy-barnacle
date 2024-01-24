from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class Listener(Protocol):
    def handle_event(self, event: Any) -> None:
        ...

class EventDispatcher:
    def __init__(self) -> None:
        self.listeners: list[Listener] = []

    def add_listener(self, listener: Listener) -> None:
        self.listeners.append(listener)

    def dispatch_event(self, event: Any) -> None:
        for listener in self.listeners:
            listener.handle_event(event)


class ChildObject:
    def __init__(self) -> None:
        self.event_dispatcher = EventDispatcher()

    def do_something(self) -> None:
        # 何かしらの処理
        print("ChildObject で何かしらの処理を実行")

        # イベントを伝達
        self.event_dispatcher.dispatch_event("ChildObject のイベント")


class ParentObject:
    def __init__(self) -> None:
        self.child_object = ChildObject()
        self.child_object.event_dispatcher.add_listener(self)

    def handle_event(self, event: Any) -> None:
        print(f"ParentObject がイベントを受信: {event}")


# 使用例
parent_obj = ParentObject()
parent_obj.child_object.do_something()
