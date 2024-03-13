#                 20                  40                  60                 79
from mod.const import opponent, IMG_BOOL_ZE, IMG_BOOL_HI, CT_KOUDOU,\
    IMG_LIFE_DAMAGE, UC_LIFE, UC_FLAIR, DMG_RESHUFFLE, POP_RESHUFFLE_SELECTED,\
    POP_OPEN, POP_ACT1, POP_ACT2
from mod.classes import Callable, Card, Delivery, moderator
from mod.card.card import auto_di
from mod.card.damage import Damage
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.pipeline_layer import PipelineLayer
from mod.card.kw.saikousei import saikousei_card

_damage = Damage(img=IMG_LIFE_DAMAGE, name="再構成ダメージです", dmg=1, from_code=
                 UC_LIFE, to_code=UC_FLAIR, attr=DMG_RESHUFFLE)

def _turn_saikousei(delivery: Delivery, hoyuusya: int) -> None:
    moderator.append(PipelineLayer(name="ターン開始時の再構成", delivery=delivery,
        hoyuusya=hoyuusya, gotoes={
POP_OPEN: lambda l, s: saikousei_card.kaiketu(delivery, hoyuusya, code=POP_ACT1),
POP_ACT1: lambda l, s: _damage.kaiketu(delivery, opponent(hoyuusya), code=POP_ACT2),
POP_ACT2: lambda l, s: moderator.pop()
        }))

_reshuffle_card = Card(img=IMG_BOOL_ZE, name="再構成", cond=auto_di, type=
                       CT_KOUDOU, kouka=_turn_saikousei)
_pass_card = Card(img=IMG_BOOL_HI, name="非", cond=auto_di, type=CT_KOUDOU)
_cards = [_reshuffle_card, _pass_card]

reshuffle_layer: Callable[[Delivery, int], OnlySelectLayer] = lambda delivery,\
    hoyuusya: OnlySelectLayer(delivery=delivery, hoyuusya=hoyuusya, name=\
    "再構成の選択", upper=_cards, code=POP_RESHUFFLE_SELECTED)
