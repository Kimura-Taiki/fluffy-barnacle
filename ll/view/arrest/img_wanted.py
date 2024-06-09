from pygame import Surface, SRCALPHA, transform, Rect

from any.pictures import IMG_WANTED
from model.kard import Kard

def img_wanted(kard: Kard) -> Surface:
    img = Surface(size=IMG_WANTED.get_size(), flags=SRCALPHA)
    img.blit(
        source=transform.rotozoom(
            surface=kard.picture(),
            angle=0.0,
            scale=1.5
        ),
        dest=(20, 160),
        area=Rect(105, 240, 300, 300)
    )
    img.blit(source=IMG_WANTED, dest=(0, 0))
    return img
