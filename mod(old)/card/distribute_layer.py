#                 20                  40                  60                 79
from pygame.surface import Surface
from pygame.math import Vector2
from functools import reduce

from mod.const import draw_aiharasuu, enforce, POP_OK, POP_OPEN, POP_CHOICED,\
    POP_DECIDED, FONT_SIZE_OSAME_NUM, UC_DUST, UC_AURA, USAGE_DEPLOYED,\
    IMG_DONOR_DUST, IMG_DONOR_AURA, POP_ACT1, POP_ACT2

from mod.classes import Any, PopStat, Card, Youso, Huda, Delivery, moderator
from mod.tf.taba_factory import TabaFactory
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.card.hakizi import hakizi

class _Donor():
    def __init__(self, name: str, youso: Youso, img: Surface) -> None:
        self.name = name
        self.youso = youso
        self.img_nega = img
        self.donation = 0

    def img(self) -> Surface:
        img_return = self.img_nega.copy()
        draw_aiharasuu(surface=img_return, dest=Vector2(img_return.get_size())/2-
                        [FONT_SIZE_OSAME_NUM/2, FONT_SIZE_OSAME_NUM/2], num=self.donation, size=FONT_SIZE_OSAME_NUM)
        return img_return

    def pour(self, amount: int) -> int:
        if amount <= 0:
            return amount
        self.donation = min(amount, self.youso.osame)
        return amount-self.donation

def _youso(layer: PipelineLayer, utuwa_code: int) -> Youso:
    return enforce(layer.delivery.utuwa_target(hoyuusya=layer.hoyuusya,
        is_mine=True, utuwa_code=utuwa_code), Youso)

def _donors(layer: PipelineLayer, amount: int) -> list[_Donor]:
    huda = enforce(layer.huda, Huda)
    rest = [_Donor(name="付与", youso=huda, img=huda.card.img),
        _Donor(name="オーラ", youso=_youso(layer, UC_AURA), img=IMG_DONOR_AURA)]
    reduce(lambda acc, donor: donor.pour(acc), rest, amount)
    return rest

def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    li = list(TabaFactory().maid_by_tuples(tuples=[(enforce(donor, _Donor).
        name, enforce(donor, _Donor).img()) for donor in layer.rest],
        delivery=delivery, hoyuusya=hoyuusya))
    moderator.append(OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya,
        name="オーラダメージの配分", upper=li, decide=True, popup=False, code=code))

def _choiced(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    name = enforce(stat.huda, Huda).card.name
    rest = [enforce(donor, _Donor) for donor in layer.rest]
    found_donor = next((donor for donor in rest if donor.name == name), None)
    if not found_donor or found_donor.donation >= found_donor.youso.osame:
        layer.moderate(PopStat(code))
        return
    for donor in rest:
        if donor == found_donor or donor.donation <= 0 or found_donor.donation\
        >= found_donor.youso.osame:
            continue
        donor.donation -= 1
        found_donor.donation += 1
        break
    layer.moderate(PopStat(code))

def _decided(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    rest = [enforce(donor, _Donor) for donor in layer.rest]
    for donor in rest:
        layer.delivery.send_ouka_to_ryouiki(hoyuusya=layer.hoyuusya, from_huda=
            donor.youso, to_code=UC_DUST, kazu=donor.donation)
    layer.huda = enforce(rest[0].youso, Huda).base
    layer.moderate(PopStat(code))

def distribute_layer(dmg: int, delivery: Delivery, hoyuusya: int,
                    huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    layer = PipelineLayer(name=f"{dmg}ダメージの配分", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_CHOICED),
POP_CHOICED: lambda l, s: _choiced(l, s, POP_OPEN),
POP_DECIDED: lambda l,s : _decided(l, s, POP_ACT1),
POP_ACT1: lambda l, s: hakizi(l, s, POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop()
        }, huda=huda, code=code)
    layer.rest = _donors(layer, dmg)
    return layer
