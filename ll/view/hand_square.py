from pygame import Surface, transform, Vector2 as V2, mouse
from math import sin, cos, radians

from any.mouse_dispatcher import mouse_dispatcher
from any.pictures import IMG_WHITE
from model.kard import Kard
from model.ui_element import UIElement
from ptc.bridge import Bridge

from ptc.square import Square
class HandSquare():
    def __init__(
            self, kard: Kard, angle: float, scale: float, center: V2,
            bridge: Bridge, canvas: Surface
    ) -> None:
        self.kard = kard
        self.angle = angle
        self.scale = scale
        self.center = center
        self.bridge = bridge
        self.canvas = canvas
        self.img = self._img()
        self.img_white = self._img_white()
        self.vertices = self._vertices()
        self.ui_element = UIElement(mousedown=self._mousedown)

    def get_hover(self) -> UIElement | None:
        inside = False
        mx, my = mouse.get_pos()
        for i in range(4):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i+1) % 4]
            if ((y1 <= my and my < y2) or (y2 <= my and my < y1)) and (mx < (x2-x1)*(my-y1)/(y2-y1)+x1):
                inside = not inside
        return self.ui_element if inside else None

    def draw(self) -> None:
        self.canvas.blit(
            source=self.img,
            dest=self.center-V2(self.img.get_size())/2
        )
        if mouse_dispatcher.hover == self.ui_element:
            self.canvas.blit(
                source=self.img_white,
                dest=self.center-V2(self.img.get_size())/2
            )

    def _img(self) -> Surface:
        return transform.rotozoom(
            surface=self.kard.picture(),
            angle=self.angle,
            scale=self.scale
        )

    def _img_white(self) -> Surface:
        return transform.rotozoom(
            surface=IMG_WHITE,
            angle=self.angle,
            scale=self.scale
        )

    def _vertices(self) -> list[V2]:
        hx, hy = V2(self.kard.picture().get_size())/2
        li = [V2(-hx, -hy), V2(hx, -hy), V2(hx, hy), V2(-hx, hy)]
        return [self._rotated_vertices(v2*self.scale) for v2 in li]

    def _rotated_vertices(self, from_v2: V2) -> V2:
        rad = radians(-self.angle)
        return V2(
            self.center.x+(cos(rad)*from_v2.x-sin(rad)*from_v2.y),
            self.center.y+(sin(rad)*from_v2.x+cos(rad)*from_v2.y),
        )

    def _mousedown(self) -> None:
        self.bridge.board.use_kard(player=self.bridge.board.turn_player, kard=self.kard)
        self.bridge.board.advance_to_next_turn()
        from ctrl.turn_starts import TurnStartsController
        TurnStartsController(bridge=self.bridge).action()