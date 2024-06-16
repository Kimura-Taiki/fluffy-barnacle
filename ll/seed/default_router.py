from any.router import Router

router = Router()

# ボード直轄の非同期処理
from ctrl.drawn_funcs import DrawnFuncsController
from ctrl.diskard_funcs import DiskardFuncsController
router.drawn_funcs_async = DrawnFuncsController(
    injector=router.bridge_injector
).action
router.diskard_funcs_async = DiskardFuncsController(
    injector=router.bridge_injector
).action

# インディース版カードの非同期処理
from ctrl.arrests import ArrestsController
from ctrl.peeps import PeepsController
from ctrl.duels import DuelsController
from ctrl.guards import GuardsController
from ctrl.protects import ProtectsController
from ctrl.exchange_kards import ExchangeKardsController
from ctrl.defeat_by_ministers import DefeatByMinistersController
from ctrl.diskard_himes import DiskardHimesController

router.arrests_async = ArrestsController(
    injector=router.bridge_injector
).action
router.peeps_async = PeepsController(
    injector=router.bridge_injector
).action
router.duels_async = DuelsController(
    injector=router.bridge_injector
).action
router.guards_async = GuardsController(
    injector=router.bridge_injector
).action
router.protects_async = ProtectsController(
    injector=router.bridge_injector
).action
router.exchange_kards_async = ExchangeKardsController(
    injector=router.bridge_injector
).action
router.defeat_by_ministers_async = DefeatByMinistersController(
    injector=router.bridge_injector
).action
router.diskard_himes_async = DiskardHimesController(
    injector=router.bridge_injector
).action
