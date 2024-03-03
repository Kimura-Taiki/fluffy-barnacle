#                 20                  40                  60                 79
from mod.const import pass_func, enforce, POP_HUYO_ELAPSED
from mod.classes import Callable, Any, Huda, PopStat, Delivery, moderator, popup_message
from mod.ol.remove_osame.single_remove import single_remove_layer, choice_layer, huyo_hudas
from mod.ol.only_select_layer import OnlySelectLayer
from mod.ol.turns_progression.pipeline_layer import PipelineLayer



class RemoveOsame():
    def __init__(self, delivery: Delivery, hoyuusya: int) -> None:
        self.delivery = delivery
        self.hoyuusya = hoyuusya
        self.name = "付与の償却"
        self.inject_func: Callable[[], None] = pass_func

    def elapse(self) -> None:
        ...

    def get_hover(self) -> Any | None:
        return None

    def open(self) -> None:
        popup_message.add("付与の納を償却します")
        # moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya))
#                 20                  40                  60                 79
        moderator.append(choice_layer(hudas=huyo_hudas(delivery=self.delivery,
            hoyuusya=self.hoyuusya), delivery=self.delivery, hoyuusya=self.
            hoyuusya))

    def close(self) -> PopStat:
        return PopStat(POP_HUYO_ELAPSED)

    def moderate(self, stat: PopStat) -> None:
        print("moderate", stat)
        if not stat.rest_taba:
            moderator.pop()
        else:
            # moderator.append(single_remove_layer(delivery=self.delivery, hoyuusya=self.hoyuusya, taba=stat.rest_taba))
            moderator.append(choice_layer(hudas=stat.rest_taba, delivery=self.
                delivery, hoyuusya=self.hoyuusya))
