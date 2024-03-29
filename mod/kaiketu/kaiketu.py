#                 20                  40                  60                 79
from mod.const import POP_OK, POP_OPEN, UC_DUST, UC_FLAIR,\
    CT_KOUGEKI, CT_KOUDOU, CT_HUYO, CT_DIV
from mod.classes import Callable, PopStat, Card, Huda, Delivery, moderator, popup_message
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.pop_stat import PopStat
from mod.ol.play_koudou import play_koudou_layer, play_div_layer

def _end(layer: PipelineLayer, stat: PopStat) -> None:
    raise EOFError("カードタイプが存在しない！")

_error_layer: Callable[[Card, Delivery, int, Huda | None, int],
PipelineLayer] = lambda c, d, h, a, i: PipelineLayer(
    "カードタイプが存在しない！", d, h, gotoes={POP_OPEN: _end})

def kaiketu(card: Card, delivery: Delivery, hoyuusya: int, huda: Huda | None=None, code: int=POP_OK) -> None:
    if card.kirihuda:
        delivery.send_ouka_to_ryouiki(hoyuusya=hoyuusya, from_mine=True, from_code=UC_FLAIR, to_mine=False, to_code=UC_DUST,
                                        kazu=card.flair(delivery, hoyuusya))
    if not card.can_play(delivery=delivery, hoyuusya=hoyuusya, popup=True):
        def _pop(layer: PipelineLayer, stat: PopStat) -> None:
            popup_message.add(f"！？解決時に「{card.name}」の使用条件を満たしていません！？")
            moderator.pop()
        moderator.append(PipelineLayer(name="解決失敗", delivery=delivery, hoyuusya=hoyuusya, gotoes={
            POP_OPEN: _pop
            }, code=code))
        return
    from mod.ol.play_kougeki.play_kougeki import play_kougeki_layer
    from mod.ol.play_huyo import play_huyo_layer
    layer = {CT_DIV: play_div_layer, CT_KOUGEKI: play_kougeki_layer, CT_KOUDOU: play_koudou_layer,
        CT_HUYO: play_huyo_layer}.get(card.type, _error_layer)(card, delivery, hoyuusya, huda, code)
    moderator.append(layer)
