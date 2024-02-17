#                 20                  40                  60                 79
from mod.const import POP_HAKIZI_DID
from mod.delivery import Delivery
from mod.huda import Huda
from mod.ol.kaiketu_layer_facotry import kaiketu_layer_factory

def _dih(delivery: Delivery, hoyuusya: int, huda: Huda) -> None:
    huda.card.hakizi(delivery, hoyuusya)

Hakizi = kaiketu_layer_factory(name="の破棄時効果", code=POP_HAKIZI_DID, dih=_dih)
