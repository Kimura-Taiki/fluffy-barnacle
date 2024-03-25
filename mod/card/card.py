#                 20                  40                  60                 79
from pygame.surface import Surface
from typing import Callable, Any, Optional

from mod.const import side_name,\
    CT_HUTEI, CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_DIV,\
    UC_FLAIR, UC_DUST, UC_MAAI, POP_OK, POP_OPEN, SC_TIKANDOKU
from mod.delivery import Delivery
from mod.popup_message import popup_message
from mod.moderator import moderator
from mod.coous.continuous import Continuous
from mod.coous.scalar_correction import applied_scalar
from mod.card.card_func import maai_text, is_meet_conditions
from mod.card.amortize import amortize_default

BoolDI = Callable[[Delivery, int], bool]
BoolDIC = Callable[[Delivery, int, 'Card'], bool]
KoukaDI = Callable[[Delivery, int], None]
SuuziDI = Callable[[Delivery, int], int]
MaaiDI = Callable[[Delivery, int], list[bool]]
TaiounizeDI = Callable[['Card', Delivery, int], 'Card']
auto_di: BoolDI = lambda delivery, hoyuusya: True
nega_di: BoolDI = lambda delivery, hoyuusya: False
auto_dic: BoolDIC = lambda delivery, hoyuusya, card: True
nega_dic: BoolDIC = lambda delivery, hoyuusya, card: False
pass_di: KoukaDI = lambda delivery, hoyuusya: None
int_di: Callable[[int], SuuziDI] = lambda i: lambda delivery, hoyuusya: i
whole_di: MaaiDI = lambda delivery, hoyuusya: [True]*11
moma_di: Callable[[int], MaaiDI] = lambda i: lambda delivery, hoyuusya: [j == i for j in range(11)]
dima_di: Callable[[int, int], MaaiDI] = lambda i, j: lambda delivery, hoyuusya: [i <= k <= j for k in range(11)]
identity_di: TaiounizeDI = lambda i, j, k: i

#                 20                  40                  60                 79
class Card():
    def __init__(self, 
    img: Surface, name: str, cond: BoolDI, type: int=CT_HUTEI, megami: int=0, 
    aura_damage_func: SuuziDI=int_di(0), aura_bar: BoolDI=nega_di,
    life_damage_func: SuuziDI=int_di(0), life_bar: BoolDI=nega_di,
    maai_list: MaaiDI=whole_di, taiouble: BoolDIC=auto_dic,
    after: Optional['Card']=None,
    kouka: KoukaDI=pass_di,
    osame: SuuziDI = int_di(0), suki: BoolDI=auto_di,
    tenkaizi: Optional['Card']=None, hakizi: Optional['Card']=None,
    amortize: Callable[[Any], None]=amortize_default, cfs: list[Continuous]=[],
    used: list[Continuous]=[],
    taiou: bool=False, zenryoku: bool=False, syuutan: bool=False,
    kirihuda: bool=False, flair: SuuziDI=int_di(0), taiounize: TaiounizeDI = identity_di,
    **kwargs: Any
    ) -> None:
        self.img, self.name, self.cond, self.type = img, name, cond, type
        self.megami = megami
        self.aura_damage_func, self.aura_bar = aura_damage_func, aura_bar
        self.life_damage_func, self.life_bar = life_damage_func, life_bar
        self.maai_list, self.taiouble = maai_list, taiouble
        self.after = after
        self.kouka =kouka
        self.osame, self.suki, self.tenkaizi, self.hakizi = osame, suki, tenkaizi, hakizi
        self.amortize, self.cfs, self.used = amortize, cfs, used
        self.taiou = taiou
        self.flair = flair
        self.zenryoku = zenryoku
        self.syuutan = syuutan
        self.kirihuda = kirihuda
        self.taiounize = taiounize
        self.kwargs = kwargs

    def kaiketu(self, delivery: Delivery, hoyuusya: int, huda: Any | None=None, code: int=POP_OK) -> None:
        if self.kirihuda:
            delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_FLAIR, to_mine=False, to_code=UC_DUST,
                                          kazu=self.flair(delivery, hoyuusya))
        if not self.can_play(delivery=delivery, hoyuusya=hoyuusya, popup=True):
            from mod.ol.pipeline_layer import PipelineLayer
            from mod.ol.pop_stat import PopStat
            def _pop(layer: PipelineLayer, stat: PopStat) -> None:
                popup_message.add(f"！？解決時に「{self.name}」の使用条件を満たしていません！？")
                moderator.pop()
            moderator.append(PipelineLayer(name="解決失敗", delivery=delivery, hoyuusya=hoyuusya, gotoes={
                POP_OPEN: _pop
                }, code=code))
            return
        if self.type == CT_KOUDOU or self.type == CT_DIV:
            from mod.ol.play_koudou import play_koudou_layer
            moderator.append(over_layer=play_koudou_layer(card=self, delivery=delivery, hoyuusya=hoyuusya, huda=huda, code=code))
        elif self.type == CT_KOUGEKI:
            from mod.ol.play_kougeki.play_kougeki import play_kougeki_layer
            moderator.append(over_layer=play_kougeki_layer(card=self, delivery=delivery, hoyuusya=hoyuusya, huda=huda, code=code))
        elif self.type == CT_HUYO:
            from mod.ol.play_huyo import play_huyo_layer
            moderator.append(play_huyo_layer(card=self, delivery=delivery, hoyuusya=hoyuusya, huda=huda, code=code))

    def is_full(self, delivery: Delivery, hoyuusya: int) -> bool:
        return not self.kirihuda or delivery.ouka_count(
            hoyuusya=hoyuusya, is_mine=True, utuwa_code=UC_FLAIR) >= self.flair(delivery, hoyuusya)

    def can_play(self, delivery: Delivery, hoyuusya: int, popup: bool=False) -> bool:
        checks: list[tuple[bool, str]] = [
            (not self.cond(delivery, hoyuusya), f"「{self.name}」の使用条件を満たしていません"),
            (self.type == CT_KOUGEKI and not self.maai_cond(delivery=delivery, hoyuusya=hoyuusya), f"「{self.name}」の適正距離から外れています"),
            (self.type == CT_KOUGEKI and applied_scalar(i=0, scalar=SC_TIKANDOKU, delivery=delivery, hoyuusya=hoyuusya) > 0,
             "弛緩毒の展開中に攻撃はできません")
        ]
        return is_meet_conditions(checks=checks, popup=popup)

    def close(self, hoyuusya: int) -> None:
        popup_message.add(f"{side_name(hoyuusya)}の「{self.name}」を解決しました")

    def maai_cond(self, delivery: Delivery, hoyuusya: int) -> bool:
        return self.maai_list(delivery, hoyuusya)[delivery.b_params.maai]

    def aura_damage(self, delivery: Delivery, hoyuusya: int) -> int | None:
        return None if self.aura_bar(delivery, hoyuusya) else self.aura_damage_func(delivery, hoyuusya)

    def life_damage(self, delivery: Delivery, hoyuusya: int) -> int | None:
        return None if self.life_bar(delivery, hoyuusya) else self.life_damage_func(delivery, hoyuusya)
