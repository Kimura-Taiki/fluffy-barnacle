#                 20                  40                  60                 79
from mod.const import CF_TRIGGER, TG_2_OR_MORE_DAMAGE, enforce
from mod.delivery import Delivery
from mod.coous.trigger import Trigger

def damage_2_or_more(delivery: Delivery, hoyuusya: int) -> None:
    effects = [enforce(cf, Trigger).effect for cf in delivery.cfs(
        type=CF_TRIGGER, hoyuusya=hoyuusya) if enforce(cf, Trigger).trigger
        == TG_2_OR_MORE_DAMAGE]
    if len(effects) == 0:
        ...
    elif len(effects) == 1:
        effects[0].kaiketu(delivery=delivery, hoyuusya=hoyuusya, huda=None, code=0)
    else:
        raise EOFError("TG_2_OR_MORE_DAMAGEで再起する効果が２つ以上になったね")
