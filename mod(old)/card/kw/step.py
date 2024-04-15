#                 20                  40                  60                 79
from mod.classes import Delivery, moderator
from mod.card.card import auto_di
from mod.card.temp_koudou import TempKoudou
from mod.ol.choice import choice_layer
from mod.card.kw.yazirusi import ya_moguri, ya_ridatu

tk_moguri = TempKoudou(name="潜り", cond=auto_di, kouka=ya_moguri.send, todo=[ya_moguri.listed()])
tk_ridatu = TempKoudou(name="離脱", cond=auto_di, kouka=ya_ridatu.send, todo=[ya_ridatu.listed()])

def each_step(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(over_layer=choice_layer(cards=[tk_moguri, tk_ridatu], delivery=delivery, hoyuusya=hoyuusya))
