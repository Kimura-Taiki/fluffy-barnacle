import pygame
from mod.card import Kougeki, auto_di, int_di, dima_di

n_1 = Kougeki(img=pygame.image.load("na_00_hajimari_a_n_1.png"), cond=auto_di,
              aura_damage=int_di(3), life_dagage=int_di(1), maai_list=dima_di(5, 9))

n_2 = Kougeki(img=pygame.image.load("na_00_hajimari_a_n_2.png"), cond=auto_di,
              aura_damage=int_di(2), life_dagage=int_di(2), maai_list=dima_di(2, 3))

n_3 = Kougeki(img=pygame.image.load("na_00_hajimari_a_n_3.png"), cond=auto_di,
              aura_damage=int_di(2), life_dagage=int_di(1), maai_list=dima_di(1, 3))

n_4 = Kougeki(img=pygame.image.load("na_00_hajimari_a_n_4.png"), cond=auto_di,
              aura_damage=int_di(3), life_dagage=int_di(2), maai_list=dima_di(1, 1))
