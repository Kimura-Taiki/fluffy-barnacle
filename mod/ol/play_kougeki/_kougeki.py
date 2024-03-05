#                 20                  40                  60                 79
from pygame.math import Vector2

from mod.const import screen, IMG_GRAY_LAYER, compatible_with, WX, WY, side_name, opponent, POP_TAIOUED, POP_OK,\
    enforce, POP_OPEN, POP_CHOICED, POP_AFTER_ATTACKED, POP_VIEWED_BANMEN, POP_RECEIVED, POP_KAIKETUED, OBAL_USE_CARD
from mod.classes import Any, PopStat, Card, Huda, Taba, Delivery, moderator,\
    popup_message
from mod.ol.view_banmen import view_youso
from mod.ol.play_kougeki._uke import uke_cards
from mod.ol.play_kougeki._taiou import taiou_hudas
from mod.ol.play_kougeki.uke_taba import uke_taba
from mod.ol.play_kougeki.taiou_taba import taiou_taba
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer
from mod.card.damage import Damage
from mod.ol.use_card_layer import use_card_layer

#                 20                  40                  60                 79
def _open(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    card = enforce(layer.card, Card)
    if not card.can_play(delivery=delivery, hoyuusya=hoyuusya, popup=True):
        moderator.pop()
        return
    upper = uke_cards(card=card, delivery=delivery, hoyuusya=hoyuusya)
    lower = taiou_hudas(card=card, delivery=delivery, hoyuusya=hoyuusya)
    if stat.switch:
        lower.clear()
    moderator.append(OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya,
        name=f"{side_name(opponent(hoyuusya))}の「{card.name}」受け選択",
        lower=lower, upper=upper, code=code))
    
def _choiced(layer: PipelineLayer, stat: PopStat, uke_code: int,
             taiou_code: int) -> None:
    huda, kougeki = enforce(stat.huda, Huda), enforce(layer.card, Card)
    if isinstance(huda.card, Damage):
        popup_message.add(f"{side_name(layer.hoyuusya)}の「{kougeki.name}」を"\
                          f"{huda.card.name}")
        huda.card.kaiketu(delivery=layer.delivery, hoyuusya=layer.hoyuusya,
                          code=uke_code)
        return
    layer.delivery.b_params.during_taiou = True
    moderator.append(use_card_layer(cards=[huda.card], name=
        f"{side_name(huda.hoyuusya)}は対応して「{huda.card.name}」を使います",
        youso=huda, mode=OBAL_USE_CARD, code=taiou_code))
#                 20                  40                  60                 79

def _taioued(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    layer.delivery.b_params.during_taiou = False
    delivery, hoyuusya = layer.delivery, layer.hoyuusya
    huda, kougeki = enforce(stat.huda, Huda), enforce(layer.card, Card)
    if not kougeki.maai_cond(delivery=delivery, hoyuusya=hoyuusya):
        popup_message.add(text=f"{side_name(hoyuusya)}の「{kougeki.name}」が"\
                          "適正距離から外れました")
        moderator.pop()
        return
    layer.card = huda.card.taiounize(kougeki, delivery, hoyuusya)
    layer.moderate(stat=PopStat(code=code, switch=True))

def play_kougeki_layer(card: Card, delivery: Delivery, hoyuusya: int,
                       huda: Any | None, code: int=POP_OK) -> PipelineLayer:
    layer = PipelineLayer(name=f"攻撃:{card.name}の使用", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_CHOICED),
POP_CHOICED: lambda l, s: _choiced(l, s, POP_KAIKETUED, POP_TAIOUED),
POP_TAIOUED: lambda l, s: _taioued(l, s, POP_OPEN),
POP_KAIKETUED: lambda l, s: moderator.pop()
        }, card=card, huda=huda, code=code)
    return layer
#                 20                  40                  60                 79

# class PlayKougeki():
#     def __init__(self, kougeki: Card, delivery: Delivery, hoyuusya: int, huda: Any | None, code: int=POP_OK,) -> None:
#         self.kougeki = kougeki
#         self.delivery = delivery
#         self.hoyuusya = hoyuusya
#         self.source_huda = huda if isinstance(huda, Huda) else None
#         self.name = f"攻撃:{kougeki.name}の使用"
#         self.inject_func = delivery.inject_view
#         self.taiou_taba: Taba = Taba()
#         self.uke_taba: Taba = Taba()
#         self.taiou_huda: Huda | None = None
#         self.code = code

#     def elapse(self) -> None:
#         screen.blit(source=self.kougeki.img, dest=-Vector2(self.kougeki.img.get_size())/2+Vector2(WX, WY)/2)
#         screen.blit(source=IMG_GRAY_LAYER, dest=[0, 0])
#         self.uke_taba.elapse()
#         self.taiou_taba.elapse()

#     def get_hover(self) -> Any | None:
#         return self.uke_taba.get_hover_huda() or self.taiou_taba.get_hover_huda() or view_youso

#     def open(self) -> None:
#         if not self.kougeki.can_play(delivery=self.delivery, hoyuusya=self.hoyuusya, popup=True):
#             moderator.pop()
#             return
#         self.uke_taba = uke_taba(kougeki=self.kougeki,
#                                  delivery=self.delivery, hoyuusya=self.hoyuusya)
#         self.taiou_taba = taiou_taba(delivery=self.delivery, hoyuusya=self.hoyuusya, kougeki=self.kougeki)
#         if self.code == POP_TAIOUED:
#             self.taiou_taba.clear()

#     def close(self) -> PopStat:
#         self.kougeki.close(hoyuusya=self.hoyuusya)
#         return PopStat(code=self.code, huda=self.source_huda)

#     def moderate(self, stat: PopStat) -> None:
#         enforce({POP_VIEWED_BANMEN: self._viewed_banmen,
#                  POP_TAIOUED: self._taioued,
#                  POP_RECEIVED: self._received,
#                  POP_AFTER_ATTACKED: self._after_attacked}.get(stat.code), type(self._taioued))(stat)

#     def _viewed_banmen(self, stat: PopStat) -> None:
#         ...

#     def _taioued(self, stat: PopStat) -> None:
#         self.delivery.b_params.during_taiou = False
#         self.taiou_huda = enforce(stat.huda, Huda)
#         self.taiou_taba.clear()
#         if not self.kougeki.maai_cond(delivery=self.delivery, hoyuusya=self.hoyuusya):
#             popup_message.add(text=f"{side_name(self.hoyuusya)}の「{self.kougeki.name}」が適正距離から外れました")
#             moderator.pop()
#             return
#         self.kougeki = self.taiou_huda.card.taiounize(self.kougeki, self.delivery, self.hoyuusya)
#         self.uke_taba = uke_taba(kougeki=self.kougeki,
#                                  delivery=self.delivery, hoyuusya=self.hoyuusya)
        
#     def _received(self, stat: PopStat) -> None:
#         if self.kougeki.after:
#             self.kougeki.after.kaiketu(
#                 delivery=self.delivery, hoyuusya=self.hoyuusya, huda=self.source_huda, code=POP_AFTER_ATTACKED)
#             return
#         moderator.pop()

#     def _after_attacked(self, stat: PopStat) -> None:
#         moderator.pop()

# compatible_with(, OverLayer)
