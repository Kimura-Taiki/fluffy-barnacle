from pygame import Vector2 as V2

vs = V2(100, 0)
ve = V2(0, 300)
print(vs.lerp(ve, .3))