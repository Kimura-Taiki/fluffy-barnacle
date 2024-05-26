from pygame import Surface, image

def picload(file: str) -> Surface:
    return image.load(f"ll/pic/{file}.png").convert_alpha()

IMG_BACK = picload("back")
IMG_REST = picload("rest")
IMG_NUM = picload("num")
