#                 20                  40                  60                 79
from typing import runtime_checkable, Protocol

from mod.const import UC_LIFE, opponent, TG_1_OR_MORE_DAMAGE,\
    TG_2_OR_MORE_DAMAGE
from mod.classes import Callable, Card, Huda, Delivery, moderator
from mod.tf.taba_factory import TabaFactory
from mod.ol.mc_layer_factory import MonoChoiceLayer
from mod.ol.pop_stat import PopStat
from mod.coous.trigger import solve_trigger_effect
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

@runtime_checkable
class _DamageArrow(Protocol):
    from_code: int
    to_code: int
    dmg: int
    attr: int

def _mouseup(huda: Huda) -> None:
    layer = moderator.last_layer()
    if not isinstance(da := huda.card, _DamageArrow):
        raise EOFError
    huda.delivery.send_ouka_to_ryouiki(hoyuusya=huda.hoyuusya, from_mine=False, from_code=da.from_code,
                                    to_mine=False, to_code=da.to_code, kazu=da.dmg)
    huda.delivery.b_params.damage_attr = da.attr
    if da.dmg >= 1 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=huda.delivery, hoyuusya=opponent(huda.hoyuusya), trigger=TG_1_OR_MORE_DAMAGE)
    if da.dmg >= 2 and da.from_code == UC_LIFE:
        solve_trigger_effect(delivery=huda.delivery, hoyuusya=opponent(huda.hoyuusya), trigger=TG_2_OR_MORE_DAMAGE)
    if moderator.last_layer() == layer:
        moderator.pop()

def _moderate(mcl: MonoChoiceLayer, stat: PopStat) -> None:
    moderator.pop()

def damage_layer(card: Card, delivery: Delivery, hoyuusya: int, code: int) -> MonoChoiceLayer:
    if not isinstance(da := card, _DamageArrow):
        raise EOFError
    mcl = MonoChoiceLayer(name=f"ダメージ解決：{da.from_code}から{da.to_code}へ{da.dmg}点", delivery=delivery, hoyuusya=hoyuusya,
                          moderate=_moderate, code=code)
    factory = TabaFactory(inject_kwargs={"mouseup": _mouseup}, is_ol=True)
    mcl.taba = factory.maid_by_cards(cards=[card], delivery=delivery, hoyuusya=hoyuusya)
    return mcl

# #                 20                  40                  60                 79
# start_phase_layer: Callable[[Delivery, ], PipelineLayer] = lambda delivery:\
#     PipelineLayer(name=f"ダメージ解決：{da.from_code}から{da.to_code}へ{da.dmg}点", delivery=delivery, gotoes={
#         POP_OPEN: _open,
#         POP_HUYO_ELAPSED: _huyo_elapsed,
#         POP_RESHUFFLE_SELECTED: _reshuffle_selected,
#         POP_RESHUFFLED: _reshuffled,
#         POP_TURN_DRAWED: _turn_drawed
#     }, code=POP_START_PHASE_FINISHED)

