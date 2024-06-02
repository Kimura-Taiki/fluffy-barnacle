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