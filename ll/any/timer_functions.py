from pygame import Rect
from time import time
from typing import Callable

from any.func import rect_fill
from any.font import MS_MINCHO_COL
from any.screen import screen, WX, FRAMES_PER_SECOND

_FONT_SIZE = 36
_DEST = (WX-380, 300)
_SIZE = (380, 40)

def timer_functions() -> tuple[Callable[[], None], Callable[[], None], Callable[[], int]]:
    log = 0.0
    times = [0.01]*FRAMES_PER_SECOND
    frame_count = 0
    def start_timer() -> None:
        nonlocal log, frame_count
        log = time()
        frame_count += 1
    def end_timer() -> None:
        nonlocal log, times
        elapsed_time = time()-log
        times.append(elapsed_time)
        times.pop(0)
        rect_fill(color="lemonchiffon", rect=Rect((_DEST), (_SIZE)))
        screen.blit(source=MS_MINCHO_COL(
            f"{(sum(times)/FRAMES_PER_SECOND*1000):.2f}ms/Loop, now{round(elapsed_time*1000, 2):.2f}", _FONT_SIZE, "black"),
            dest=_DEST)
    def frames() -> int:
        return frame_count
    return start_timer, end_timer, frames
start_timer, end_timer, frames = timer_functions()

def make_ratio_func(wait: int) -> Callable[[], float]:
    start = frames()
    def ratio() -> float:
        return min(1.0, max((frames()-start)/wait, 0.0))
    return ratio

def make_triangle_wave_func(period: int) -> Callable[[], float]:
    start = frames()
    def triangle_wave() -> float:
        phase = (frames()-start) % period
        return abs(phase-period/2)/(period/2)
    return triangle_wave