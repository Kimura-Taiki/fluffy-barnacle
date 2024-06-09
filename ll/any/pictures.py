from pygame import Surface, image

def picload(file: str) -> Surface:
    return image.load(f"ll/pictures/{file}.png").convert_alpha()

IMG_BG = picload("bg")

IMG_BACK = picload("back")
IMG_WHITE = picload("white")
IMG_REST = picload("rest")
IMG_NUM = picload("num")
IMG_BRIGHT = picload("bright")
IMG_SHIELD = picload("shield")
IMG_DUEL = picload("duel")
IMG_PEEP = picload("peep")
IMG_WANTED = picload("wanted")
IMG_HAZURE = picload("hazure")
IMG_CHAIN_L = picload("chain_l")
IMG_CHAIN_R = picload("chain_r")