from pygame.surface import Surface
from pygame.math import Vector2

from mod.const import screen, WX, WY, BLACK, WHITE, MS_MINCHO_32PT

class _Queue:
    def __init__(self, text: str, color: tuple[int, int, int] = BLACK) -> None:
        self.img_text = MS_MINCHO_32PT(text)
        self.img_shadow = Surface(self.img_text.get_size())
        self.img_shadow.fill(WHITE)
        self.lifetime: int = 60
        self.coord = Vector2(WX/2, WY-240)-Vector2(self.img_text.get_size())/2

    def draw(self) -> None:
        self.img_shadow.set_alpha(128)
        screen.blit(source=self.img_shadow, dest=self.coord)
        self.img_text.set_alpha(255)
        screen.blit(source=self.img_text, dest=self.coord)

class PopupMessage:
    def __init__(self) -> None:
        self.queues: list[_Queue] = []

    def add(self, text: str) -> None:
        add = _Queue(text=text)
        dx = add.img_text.get_height()+5
        for queue in self.queues:
            queue.coord.y -= dx
        self.queues.append(add)

    def draw(self) -> None:
        for queue in self.queues:
            queue.draw()

    def elapse(self) -> None:
        for queue in self.queues[::-1]:
            queue.lifetime -= 1
            if queue.lifetime <= 0:
                self.queues.remove(queue)

popup_message = PopupMessage()