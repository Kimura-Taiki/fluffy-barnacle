#                 20                  40                  60                 79
from mod.const import enforce, opponent, TC_YAMAHUDA, IMG_AURA_DAMAGE,\
    IMG_LIFE_DAMAGE, UC_AURA, UC_DUST, UC_LIFE, UC_FLAIR, DMG_SYOUSOU,\
    POP_OPEN, POP_SYOUSOU_SELECTED, POP_SYOUSOU_DAMAGED, POP_TURN_DRAWED
from mod.classes import Callable, PopStat, Huda, Delivery, moderator, popup_message
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer
from mod.card.damage import Damage

def _open(layer: PipelineLayer, stat: PopStat) -> None:
    popup_message.add("カードを２枚引きます")
    layer.count = 0
    _draw(layer=layer, stat=stat)

def _draw(layer: PipelineLayer, stat: PopStat) -> None:
    if layer.count >= 2:
        moderator.pop()
        return
    layer.count += 1
    if len(enforce(layer.delivery.taba_target(hoyuusya=layer.hoyuusya,
                     is_mine=True, taba_code=TC_YAMAHUDA), list)) > 0:
        layer.delivery.hand_draw(hoyuusya=layer.hoyuusya, is_mine=True)
        _draw(layer=layer, stat=stat)
    else:
        cards = [_adc(), _ldc()] if layer.delivery.ouka_count(hoyuusya=layer.
            hoyuusya, is_mine=True, utuwa_code=UC_AURA) > 0 else [_ldc()]
        moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=
            layer.hoyuusya, name="焦燥ダメージ", upper=cards, code=
            POP_SYOUSOU_SELECTED))

def _syousou_selected(layer: PipelineLayer, stat: PopStat) -> None:
    huda = enforce(stat.huda, Huda)
    popup_message.add(f"焦燥で{huda.card.name}が削れます")
    huda.card.kaiketu(delivery=layer.delivery, hoyuusya=opponent(layer.hoyuusya), code=POP_SYOUSOU_DAMAGED)

def _adc() -> Damage:
    return Damage(img=IMG_AURA_DAMAGE, name="オーラ", dmg=1, from_code=UC_AURA, to_code=UC_DUST, attr=DMG_SYOUSOU)

def _ldc() -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="ライフ", dmg=1, from_code=UC_LIFE, to_code=UC_FLAIR, attr=DMG_SYOUSOU)

turn_draw_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="手札を２枚引く", delivery=delivery, gotoes={
        POP_OPEN: _open,
        POP_SYOUSOU_SELECTED: _syousou_selected,
        POP_SYOUSOU_DAMAGED: _draw
    }, code=POP_TURN_DRAWED)
