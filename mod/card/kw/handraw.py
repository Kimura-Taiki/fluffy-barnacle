#                 20                  40                  60                 79
from mod.const import enforce, opponent, TC_YAMAHUDA, TC_TEHUDA, UC_AURA,\
    UC_DUST, UC_LIFE, UC_FLAIR, DMG_SYOUSOU, IMG_AURA_DAMAGE, IMG_LIFE_DAMAGE,\
    POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4
from mod.classes import PopStat, Huda, Delivery, moderator, popup_message
from mod.card.damage import Damage
from mod.ol.pipeline_layer import PipelineLayer
from mod.ol.only_select_layer import OnlySelectLayer

def handraw_layer(delivery: Delivery, hoyuusya: int, code: int) -> PipelineLayer:
    return PipelineLayer("カードを１枚引く", delivery, hoyuusya, gotoes={
POP_OPEN: lambda l, s: _open(l, s, POP_ACT1, POP_ACT2),
POP_ACT1: lambda l, s: _draw(l, s, POP_ACT4),
POP_ACT2: lambda l, s: _syousou(l, s, POP_ACT3),
POP_ACT3: lambda l, s: _damage(l, s, POP_ACT4),
POP_ACT4: lambda l, s: moderator.pop()
    }, code=code)

def _is_yamahuda(delivery: Delivery, hoyuusya: int) -> bool:
    return len(enforce(delivery.taba_target(hoyuusya=hoyuusya, is_mine=True,
        taba_code=TC_YAMAHUDA), list)) > 0

def _open(layer: PipelineLayer, stat: PopStat, draw_code: int,
          syousou_code: int) -> None:
    layer.moderate(PopStat(draw_code if _is_yamahuda(layer.delivery, layer.
        hoyuusya) else syousou_code))

def _draw(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    draw_huda = layer.delivery.taba_target(hoyuusya=layer.hoyuusya,
        is_mine=True, taba_code=TC_YAMAHUDA)[0]
    layer.delivery.send_huda_to_ryouiki(huda=draw_huda, is_mine=True,
        taba_code=TC_TEHUDA)
    layer.moderate(PopStat(code))

def _adc() -> Damage:
    return Damage(img=IMG_AURA_DAMAGE, name="オーラ", dmg=1, from_code=UC_AURA,
                  to_code=UC_DUST, attr=DMG_SYOUSOU)

def _ldc() -> Damage:
    return Damage(img=IMG_LIFE_DAMAGE, name="ライフ", dmg=1, from_code=UC_LIFE,
                  to_code=UC_FLAIR, attr=DMG_SYOUSOU)

def _syousou(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    cards = [_adc(), _ldc()] if layer.delivery.ouka_count(hoyuusya=
        layer.hoyuusya, is_mine=True, utuwa_code=UC_AURA) > 0 else [_ldc()]
    moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
        hoyuusya, name="焦燥ダメージの選択", upper=cards, code=code))

def _damage(layer: PipelineLayer, stat: PopStat, code: int) -> None:
    damage = enforce(stat.huda, Huda).card
    popup_message.add(f"焦燥で{damage.name}が削れます")
    damage.kaiketu(delivery=layer.delivery, hoyuusya=
        opponent(layer.hoyuusya), code=code)
