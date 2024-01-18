# 手札, 切り札, 捨札&伏札, 山札

# 集中, オーラ, フレア, ライフ
# (未使用&追加&除外)

from pygame.math import Vector2

print(Vector2.__bases__)
v = Vector2(5, 12)
print(v.length(), v[0], v[1])


data=[Huda(img=v, angle=angle_func(i, j)) for i, v in enumerate(surfaces)]
for huda in data:
    huda.belongs_to = data

return (data := [Huda(img=v, angle=angle_func(i, j), belongs_to=data) for i, v in enumerate(surfaces)])
