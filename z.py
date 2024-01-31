from mod.card import Card, auto_di
from mod.const import IMG_BACK

back = Card(img=IMG_BACK, name="伏せ札", cond=auto_di)
back.zzz = 55

print(back)
print(back.zzz)