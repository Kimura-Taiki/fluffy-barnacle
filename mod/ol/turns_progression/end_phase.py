#                 20                  40                  60                 79
from typing import Callable

from mod.const import pass_func, POP_END_PHASE_FINISHED, POP_END_TRIGGERED,\
    POP_DISCARDED, TG_END_PHASE, enforce, TC_TEHUDA, TC_HUSEHUDA
from mod.delivery import Delivery, duck_delivery
from mod.ol.pop_stat import PopStat
from mod.moderator import moderator
from mod.youso import Youso
from mod.popup_message import popup_message
from mod.coous.trigger import solve_trigger_effect
from mod.ol.only_select_layer import OnlySelectLayer
from mod.huda.huda import Huda
from mod.ol.turns_progression.pipeline_layer import PipelineLayer

def _end_triggered(layer: PipelineLayer, stat: PopStat) -> None:
    _check_discard(layer=layer)

def _discarded(layer: PipelineLayer, stat: PopStat) -> None:
    layer.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_HUSEHUDA)
    _check_discard(layer=layer)

def _check_discard(layer: PipelineLayer) -> None:
    tehuda = enforce(layer.delivery.taba_target(hoyuusya=layer.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), list)
    if len(tehuda) <= layer.delivery.b_params.tehuda_max:
        popup_message.add("ターンを終了します")
        moderator.pop()
        return
    moderator.append(OnlySelectLayer(delivery=layer.delivery, hoyuusya=layer.
        hoyuusya, name="超過手札の破棄", lower=tehuda, code=POP_DISCARDED))

end_phase_layer: Callable[[Delivery], PipelineLayer] = lambda delivery:\
    PipelineLayer(name="終了フェイズ", delivery=delivery, gotoes={
        POP_END_TRIGGERED: _end_triggered,
        POP_DISCARDED: _discarded
    },code=POP_END_PHASE_FINISHED)

class EndPhase():
    def __init__(self, inject_func: Callable[[], None]=pass_func, delivery: Delivery=duck_delivery) -> None:
        self.name = "終了フェイズ"
        self.inject_func: Callable[[], None] = inject_func
        self.delivery = delivery
        self.hoyuusya = delivery.turn_player

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Youso | None:
        return None

    def open(self) -> None:
        solve_trigger_effect(delivery=self.delivery, hoyuusya=self.hoyuusya, trigger=TG_END_PHASE, code=POP_END_TRIGGERED)
        if moderator.last_layer() == self:
            self.moderate(PopStat(code=POP_END_TRIGGERED))

    def close(self) -> PopStat:
        return PopStat(POP_END_PHASE_FINISHED)

    def moderate(self, stat: PopStat) -> None:
        enforce({POP_END_TRIGGERED: self._end_triggered,
                 POP_DISCARDED: self._discarded
                 }.get(stat.code), type(self.moderate))(stat=stat)

    def _end_triggered(self, stat: PopStat) -> None:
        self._check_discard()

    def _discarded(self, stat: PopStat) -> None:
        self.delivery.send_huda_to_ryouiki(huda=enforce(stat.huda, Huda).base, is_mine=True, taba_code=TC_HUSEHUDA)
        self._check_discard()

    def _check_discard(self) -> None:
        tehuda = enforce(self.delivery.taba_target(hoyuusya=self.hoyuusya, is_mine=True, taba_code=TC_TEHUDA), list)
        if len(tehuda) <= self.delivery.b_params.tehuda_max:
            popup_message.add("ターンを終了します")
            moderator.pop()
            return
        moderator.append(OnlySelectLayer(delivery=self.delivery, hoyuusya=self.
            hoyuusya, name="超過手札の破棄", lower=tehuda, code=POP_DISCARDED))
