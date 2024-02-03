import pygame
from pygame.surface import Surface
from typing import Callable

pygame.init()


# ゲーム画面のサイズを設定
# screen_width, screen_height = 1280, 720
screen_width, screen_height = 60*10, 60*4
screen = pygame.display.set_mode((screen_width, screen_height))

AIHARA_KURO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (0, 0, 0))
AIHARA_SIRO: Callable[[str, int], Surface] = lambda s, i: pygame.font.Font("Aiharahudemojikaisho_free305.ttf", i).render(s, True, (255, 255, 255))
IMG_YATUBA_BG = pygame.image.load("pictures/yatuha_bg.png").convert_alpha()

def aihara_draw(text: str, size: int, color: tuple[int, int, int], x: int=0, y: int=0) -> None:
    source=pygame.font.Font("Aiharahudemojikaisho_free305.ttf", size).render(text, True, color)
    screen.blit(source=source, dest=[30-source.get_width()/2+x, 30-source.get_height()/2+y])

# 画面に表示する何かしらのものを描画（例：赤い四角形）
# screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])

screen.fill(color=(64, 64, 64))
for i in range(40):
    s = str(i)
    x = i%10*60
    y = i//10*60
    aihara_draw(text=s, size=56, color=(0, 0, 0), x=x-2, y=y-2)
    aihara_draw(text=s, size=56, color=(0, 0, 0), x=x-2, y=y+2)
    aihara_draw(text=s, size=56, color=(0, 0, 0), x=x+2, y=y-2)
    aihara_draw(text=s, size=56, color=(0, 0, 0), x=x+2, y=y+2)
    aihara_draw(text=s, size=56, color=(255, 255, 255), x=x, y=y)

# source = AIHARA_KURO("56", 56)
# x = 30-source.get_width()/2
# y = 30-source.get_height()/2
# screen.blit(source=source, dest=[x, y])
# pygame.draw.rect(screen, (255, 0, 0), (100, 100, 200, 200))

pygame.display.flip()

# スクリーンショットを撮る
pygame.image.save(screen, "screenshot.png")
# pygame.quit()

# イベントループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
