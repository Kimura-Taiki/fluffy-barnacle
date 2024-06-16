from any.router import Router

router = Router()

# ボード直轄の非同期処理
from ctrl.bright_kards import BrightKardsController
from ctrl.draw_kards import DrawKardsController
from ctrl.turn_starts import TurnStartsController
from ctrl.setups import SetupsController
from ctrl.win_by_strengths import WinByStrengthsController
from ctrl.win_by_survivals import WinBySurvivalsController

router.setups_async = SetupsController(
    injector=router.bridge_injector
).action
router.draw_kards_async = DrawKardsController(
    injector=router.bridge_injector
).action
router.turn_starts_async = TurnStartsController(
    injector=router.bridge_injector
).action
router.use_kards_async = BrightKardsController(
    injector=router.bridge_injector
).action
router.win_by_strengths_async = WinByStrengthsController(
    injector=router.bridge_injector
).action
router.win_by_survivals_async = WinBySurvivalsController(
    injector=router.bridge_injector
).action

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
