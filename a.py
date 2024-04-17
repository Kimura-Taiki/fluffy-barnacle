import pygame

from mod.const.screen import clock, FRAMES_PER_SECOND
from mod.router import router
from mod.banmen_view import BanmenView
from mod.banmen import Banmen
from mod.card import Card
from zh.z00_0 import n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9

bmn = Banmen(cards=[Card(zh=zh) for zh in [n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9]])
view = BanmenView(bmn=bmn)

def mainloop() -> None:
    router.resolve_pygame_events()
    view.draw()
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

while True:
    mainloop()
