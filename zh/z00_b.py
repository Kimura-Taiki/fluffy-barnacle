from pygame import Surface, image

from mod.const.megami import MG_HONOKA
from mod.zyouhou import Zyouhou

_MEGAMI = MG_HONOKA
_ADDRESS = "na_00_hajimari_b"
def img_card(add: str) ->  Surface:
    return image.load(f"cards/{_ADDRESS}_{add}.png")

n_1 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_1"), name="花弁刃")

n_2 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_2"), name="桜刀")

n_3 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_3"), name="瞬霊式")

n_4 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_4"), name="返し斬り")

n_5 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_5"), name="歩法")

n_6 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_6"), name="桜寄せ")

n_7 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_7"), name="光輝収束")

n_8 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_8"), name="光の刃")

n_9 = Zyouhou(siyousya={_MEGAMI}, img=img_card("n_9"), name="精霊連携")

s_1 = Zyouhou(siyousya={_MEGAMI}, img=img_card("s_1"), name="光満ちる一刀")

s_2 = Zyouhou(siyousya={_MEGAMI}, img=img_card("s_2"), name="花吹雪の景色")

s_3 = Zyouhou(siyousya={_MEGAMI}, img=img_card("s_3"), name="精霊たちの風")

s_4 = Zyouhou(siyousya={_MEGAMI}, img=img_card("s_4"), name="煌めきの乱舞")
