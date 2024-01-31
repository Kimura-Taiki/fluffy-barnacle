

class ViewBanmen():
    name: str = "------"
    inject_func: Callable[[], None] = pass_func
    delivery: Delivery = duck_delivery

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        ...

    def open(self) -> None:
        ...

    def close(self) -> int:
        ...

    def moderate(self, stat: int) -> None:
        ...
