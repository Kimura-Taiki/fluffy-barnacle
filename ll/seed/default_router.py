from any.router import Router
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.guards import GuardsController

router = Router()
router.exchange_kards_async = ExchangeKardsController(
    injector=router.bridge_injector
).action
router.guards_async = GuardsController(
    injector=router.bridge_injector
).action
