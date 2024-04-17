from pygame import Surface, image

from mod.const.megami import MG_UTURO
from mod.zyouhou import Zyouhou

_ADDRESS = "na_00_hajimari_a"
def img_card(add: str) ->  Surface:
    return image.load(f"cards/{_ADDRESS}_{add}.png")

n_1 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_1"), name="投射")

n_2 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_2"), name="脇斬り")

n_3 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_3"), name="牽制")

n_4 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_4"), name="背中刺し")

n_5 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_5"), name="二刀一閃")

n_6 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_6"), name="歩法")

n_7 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_7"), name="潜り")

n_8 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_8"), name="患い")

n_9 = Zyouhou(siyousya={MG_UTURO}, img=img_card("n_9"), name="陰の罠")

s_1 = Zyouhou(siyousya={MG_UTURO}, img=img_card("s_1"), name="数多ノ刃")

s_2 = Zyouhou(siyousya={MG_UTURO}, img=img_card("s_2"), name="闇凪ノ声")

s_3 = Zyouhou(siyousya={MG_UTURO}, img=img_card("s_3"), name="苦ノ外套")

s_4 = Zyouhou(siyousya={MG_UTURO}, img=img_card("s_4"), name="奪イノ茨")
