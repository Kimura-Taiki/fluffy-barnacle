from any.router import Router
from ctrl.duels import DuelsController
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.guards import GuardsController
from ctrl.protects import ProtectsController

router = Router()
router.duels_async = DuelsController(
    injector=router.bridge_injector
).action
router.exchange_kards_async = ExchangeKardsController(
    injector=router.bridge_injector
).action
router.guards_async = GuardsController(
    injector=router.bridge_injector
).action
router.protects_async = ProtectsController(
    injector=router.bridge_injector
).action