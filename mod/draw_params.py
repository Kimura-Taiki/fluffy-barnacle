
#                 20                  40                  60                 79
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from mod.huda import Huda

class DrawParams(NamedTuple):
    usage: int = -1
    osame: int = -1
    aura_damage: int = -1
    life_damage: int = -1

    @classmethod
    def made_by_huda(cls, huda: 'Huda') -> 'DrawParams':
        return DrawParams(
            usage=huda.usage, osame=huda.osame, aura_damage=huda.card.
            aura_damage(huda.delivery, huda.hoyuusya), life_damage=huda.card.
            life_damage(huda.delivery, huda.hoyuusya))
