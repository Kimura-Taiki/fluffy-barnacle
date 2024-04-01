#                 20                  40                  60                 79
from mod.const import enforce, USAGE_UNUSED, USAGE_USED
from mod.classes import PopStat, Huda, moderator
from mod.ol.pipeline_layer import PipelineLayer

def hakizi(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    huda = enforce(layer.huda, Huda).base
    if huda.osame == 0:
        huda.usage = USAGE_USED if huda.card.kirihuda else USAGE_UNUSED
        if huda.card.hakizi:
            huda.card.hakizi.kaiketu(delivery=huda.delivery, hoyuusya=huda.
                                     hoyuusya, code=code)
            return
    if moderator.last_layer() == layer:
        layer.moderate(PopStat(code=code))
