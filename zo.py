from pygame import Rect, Vector2 as V2

r1 = Rect(10, 20, 30, 40)
r2 = Rect((10, 20), (30, 40))
r3 = Rect(V2(10, 20), V2(30, 40))
r4 = Rect(r1)

print(r1, r2, r3, r4)
print(r1.left, r1.right, r1.top, r1.bottom, r1.centerx, r1.centery, r1.topleft, r1.bottomright, r1.center)