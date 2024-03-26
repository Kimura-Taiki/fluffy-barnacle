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

END_LAYER: Callable[[int], PipelineLayer] = lambda code: PipelineLayer(
    name="即終了", delivery=duck_delivery, gotoes={
        POP_OPEN: lambda l, s: moderator.pop()
    }, code=code)
