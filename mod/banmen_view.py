from mod.const.screen import screen, IMG_YATUBA_BG

class BanmenView():
    def draw(self) -> None:
        screen.blit(source=IMG_YATUBA_BG, dest=[0, 0])
