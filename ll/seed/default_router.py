from any.router import Router
from ctrl.arrests import ArrestsController
from ctrl.defeat_by_ministers import DefeatByMinistersController
from ctrl.duels import DuelsController
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.guards import GuardsController
from ctrl.peeps import PeepsController
from ctrl.protects import ProtectsController

router = Router()
router.arrests_async = ArrestsController(
    injector=router.bridge_injector
).action
router.defeat_by_ministers_async = DefeatByMinistersController(
    injector=router.bridge_injector
).action
router.duels_async = DuelsController(
    injector=router.bridge_injector
).action
router.exchange_kards_async = ExchangeKardsController(
    injector=router.bridge_injector
).action
router.guards_async = GuardsController(
    injector=router.bridge_injector
).action
router.peeps_async = PeepsController(
    injector=router.bridge_injector
).action
router.protects_async = ProtectsController(
    injector=router.bridge_injector
).action