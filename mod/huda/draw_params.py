
#                 20                  40                  60                 79
from typing import NamedTuple, TYPE_CHECKING

from mod.const import enforce
from mod.card.card_func import maai_text
from mod.coous.attack_correction import applied_kougeki

if TYPE_CHECKING:
    from mod.huda.huda import Huda

class DrawParams(NamedTuple):
    usage: int = -1
    osame: int = -1
    aura_damage: int | None = None
    life_damage: int | None = None
    maai_text: str = ""

    @classmethod
    def made_by_huda(cls, huda: 'Huda') -> 'DrawParams':
        applied = applied_kougeki(huda.card, huda.delivery, huda.hoyuusya)
        return DrawParams(
            usage=huda.usage, osame=huda.osame,
            aura_damage=applied.aura_damage(huda.delivery, huda.hoyuusya),
            life_damage=applied.life_damage(huda.delivery, huda.hoyuusya),
            maai_text=maai_text(applied.maai_list(huda.delivery, huda.hoyuusya))
        )
