from pygame import Surface, image

def picload(file: str) -> Surface:
    return image.load(f"ll/pic/{file}.png").convert_alpha()

IMG_BACK = picload("back")
IMG_REST = picload("rest")
IMG_NUM = picload("num")

# IMG_BACK = image.load("ll/pic/back.png").convert_alpha()
# IMG_REST = image.load("ll/pic/rest.png").convert_alpha()
# IMG_NUM = image.load("ll/pic/num.png").convert_alpha()
