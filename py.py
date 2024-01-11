import pygame
from pygame.locals import QUIT
import sys
import time

from mod.const import UTURO, CARDS, screen, clock, FRAMES_PER_SECOND, MS_MINCHO
from mod.tehuda import Tehuda
from mod.controller import controller

tehuda = Tehuda.made_by_files(surfaces=[UTURO(i) for i in range(1, CARDS+1)])
controller.get_hover = tehuda.get_hover_huda
times = [1.0]*FRAMES_PER_SECOND

def mainloop() -> None:
    start_time = time.time()  # 一周期の開始時刻を記録

    controller.resolve_pygame_events()
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         pygame.quit()
    #         sys.exit()
    screen.fill(color=(255, 255, 128))
    tehuda.elapse()
    controller.mouse_over()

    end_time = time.time()  # 一周期の終了時刻を記録
    elapsed_time = end_time - start_time
    times.append(elapsed_time)
    times.pop(0)
    screen.blit(source=MS_MINCHO(f"One loop time: {round(elapsed_time*1000, 3):.3f} ms", 32), dest=[0, 0])
    screen.blit(source=MS_MINCHO(f"Frame time: {(sum(times)/FRAMES_PER_SECOND*1000):.3f} ms", 32), dest=[0, 40])
    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)


while True:
    mainloop()
