import traceback

import arrow

from c4_sign.consts import DEV_MODE
from c4_sign.lib.canvas import Canvas
from c4_sign.loading_manager import LoadingManager
from c4_sign.screen_tasks.error import ErrorScreenTask
from c4_sign.ScreenManager import ScreenManager

_screen = None
_screen_manager = ScreenManager()
_last_update = arrow.now()
_canvas = Canvas()


def init_matrix(simulator):
    global _screen
    if simulator:
        from c4_sign.lib.screen.simulator import SimulatorScreen

        _screen = SimulatorScreen()
    else:
        from c4_sign.lib.screen.matrix import MatrixScreen

        _screen = MatrixScreen()
    lm = LoadingManager(_screen)
    _screen_manager.update_tasks(lm)


def screen_active():
    if DEV_MODE:
        return True
    now = arrow.now()
    # normal hours! between 6 am and midnight.
    return now.hour >= 6 and now.hour < 24


def update_screen():
    global _screen, _canvas, _last_update, _screen_manager

    now = arrow.now()
    delta_t = now - _last_update
    _last_update = now

    text = _screen_manager.get_lcd_text()
    _screen.update_lcd(text)

    # clear canvas
    canvas = _canvas
    canvas.clear()

    # brightness
    if screen_active():
        _screen.brightness = 100
    else:
        _screen.brightness = 0
        _screen.update_display(canvas)
        return  # don't draw anything!

    # draw stuff
    try:
        _screen_manager.draw(canvas, delta_t)
    except Exception as e:
        print("ERROR: ", e)
        print("Traceback:" + "".join(traceback.format_tb(e.__traceback__)))
        print(e.__traceback__.tb_frame.f_code.co_filename, e.__traceback__.tb_lineno)
        _screen_manager.override_current_task(ErrorScreenTask(e))

    _screen.update_display(canvas)
    _screen.debug_info(
        fps=1 / delta_t.total_seconds(),
        brightness=_screen.brightness,
        current_task=_screen_manager.current_task.__class__.__name__,
        tasks=[t.__class__.__name__ for t in _screen_manager.tasks],
        task_time_elapsed=(
            _screen_manager.current_task.elapsed_time.total_seconds() if _screen_manager.current_task else None
        ),
        task_suggested_run_time=(
            _screen_manager.current_task.suggested_run_time.total_seconds() if _screen_manager.current_task else None
        ),
        task_max_run_time=(
            _screen_manager.current_task.max_run_time.total_seconds() if _screen_manager.current_task else None
        ),
    )
    _screen.debug_override(_screen_manager)
