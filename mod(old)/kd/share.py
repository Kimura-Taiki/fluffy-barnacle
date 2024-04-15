#                 20                  40                  60                 79
import pygame
from copy import copy

from mod.const import enforce, POP_OK, POP_OPEN, POP_ACT1, POP_ACT2, POP_ACT3, POP_ACT4, POP_ACT5, POP_CHOICED, POP_KAIKETUED,\
    TC_HUSEHUDA, UC_SYUUTYUU, UC_ZYOGAI, OBAL_KIHONDOUSA, OBAL_SYUUTYUU,\
    OBAL_USE_CARD, USAGE_USED, USAGE_DEPLOYED,\
    TC_MISIYOU, TC_YAMAHUDA, TC_SUTEHUDA, POP_CLOSED,\
    IMG_ZENRYOKUIZE
from mod.classes import Any, Callable, PopStat, Card, Youso, Huda, Taba, moderator,\
    popup_message
from mod.delivery import Delivery, duck_delivery
from mod.ol.pipeline_layer import PipelineLayer, _type_dummy
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.choice import choice_layer
from mod.card.card_func import is_meet_conditions

END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)

def can_kd(delivery: Delivery, hoyuusya: int, popup: bool = False) -> bool:
    checks: list[tuple[bool, str]] = [
        (delivery.m_params(hoyuusya).played_zenryoku, "既に全力行動しています"),
        (delivery.m_params(hoyuusya).played_syuutan, "既に終端行動しています"),
        (delivery.b_params.phase_ended, "フェイズが終了しています"),
    ]
    return is_meet_conditions(checks=checks, popup=popup)
