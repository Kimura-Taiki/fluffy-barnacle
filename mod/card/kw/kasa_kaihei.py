#                 20                  40                  60                 79
from random import shuffle

from mod.const import enforce, TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA,\
    USAGE_DEPLOYED, POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import PopStat, Huda, Taba, Delivery, moderator
from mod.card.temp_koudou import TempKoudou, auto_di
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.setti import setti_layer

def _saikousei_hudas(delivery: Delivery, hoyuusya: int) -> list[Huda]:
    taba1, taba2, taba3 = [enforce(delivery.taba(hoyuusya=hoyuusya,
        taba_code=taba_code), Taba) for taba_code in
        [TC_YAMAHUDA, TC_HUSEHUDA, TC_SUTEHUDA]]
    moto = list(taba1)+list(taba2)+[
        huda for huda in taba3 if huda.usage!= USAGE_DEPLOYED]
    shuffle(moto)
    return moto

def _make_yamahuda(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    for huda in _saikousei_hudas(layer.delivery, layer.hoyuusya):
        layer.delivery.send_huda_to_ryouiki(huda=huda, is_mine=True,
                                            taba_code=TC_YAMAHUDA)
    layer.moderate(PopStat(code))

def saikousei(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer("再構成", delivery, hoyuusya, gotoes={
        POP_OPEN: lambda l, s: moderator.append(setti_layer(l, s, POP_ACT1)),
        POP_ACT1: lambda l, s: _make_yamahuda(l, s, POP_ACT2),
        POP_ACT2: lambda l, s: moderator.pop()
    }))

saikousei_card = TempKoudou(name="純粋再構成", cond=auto_di, kouka=saikousei)