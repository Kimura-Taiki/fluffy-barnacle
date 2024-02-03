import pygame
import sys

# 画像の読み込み
# life = pygame.image.load("pictures/area_life.png")
from mod.card import TempCard, auto_di
tc = TempCard(name="潜り", cond=auto_di)
from mod.const import IMG_HAKUSI

def main(): # メインループ
    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((255, 255, 255))
        screen.blit(source=tc.img, dest=[0, 0])
        screen.blit(source=IMG_HAKUSI, dest=[400, 0])

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()