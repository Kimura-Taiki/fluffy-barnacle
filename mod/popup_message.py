from pygame.surface import Surface
from pygame.math import Vector2

from mod.const import screen, WX, WY, BLACK, WHITE, MS_MINCHO_32PT

class _Queue:
    def __init__(self, text: str, color: tuple[int, int, int] = BLACK) -> None:
        self.img_text = MS_MINCHO_32PT(text)
        self.img_shadow = Surface(self.img_text.get_size())
        self.img_shadow.fill(WHITE)
        self.lifetime: int = 90
        self.coord = Vector2(WX/2, WY-240)-Vector2(self.img_text.get_size())/2

    def draw(self, dy: float) -> None:
        self.img_shadow.set_alpha(255-abs(self.lifetime-82)*16 if self.lifetime >= 74 else 128 if self.lifetime >= 16 else self.lifetime*8)
        screen.blit(source=self.img_shadow, dest=self.coord+[0, dy])
        self.img_text.set_alpha(255 if self.lifetime >= 16 else self.lifetime*16)
        screen.blit(source=self.img_text, dest=self.coord+[0, dy])

class PopupMessage:
    def __init__(self) -> None:
        self.queues: list[_Queue] = []
        self.shifttime = 0
        self.dy = 0.0

    def add(self, text: str) -> None:
        add = _Queue(text=text)
        self.dy = add.img_text.get_height()+5
        for queue in self.queues:
            queue.coord.y -= self.dy
        self.queues.append(add)
        self.shifttime = 10

    def draw(self) -> None:
        for queue in self.queues:
            queue.draw(dy=self.dy)

    def elapse(self) -> None:
        for queue in self.queues[::-1]:
            queue.lifetime -= 1
            if queue.lifetime <= 0:
                self.queues.remove(queue)
        self.shifttime -= 1
        self.dy = self.dy*(self.shifttime-1)/self.shifttime if self.shifttime > 0 else 0

popup_message = PopupMessage()