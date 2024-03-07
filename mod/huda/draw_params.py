
#                 20                  40                  60                 79
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from mod.huda.huda import Huda

class DrawParams(NamedTuple):
    usage: int = -1
    osame: int = -1
    aura_damage: int | None = None
    life_damage: int | None = None
    maai: list[bool] = []

    @classmethod
    def made_by_huda(cls, huda: 'Huda') -> 'DrawParams':
        return DrawParams(
            usage=huda.usage, osame=huda.osame,
            aura_damage=huda.card.aura_damage(huda.delivery, huda.hoyuusya),
            life_damage=huda.card.life_damage(huda.delivery, huda.hoyuusya),
            maai=huda.card.maai_list(huda.delivery, huda.hoyuusya)
        )
