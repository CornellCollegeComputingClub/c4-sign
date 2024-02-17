import traceback
import arrow
from c4_sign.ScreenManager import ScreenManager
from c4_sign.lib.canvas import Canvas

from c4_sign.screen_tasks.error import ErrorScreenTask
_screen = None
_screen_manager = ScreenManager()
_last_update = arrow.now()


def init_matrix(simulator):
    global _screen
    if simulator:
        from c4_sign.lib.screen.simulator import SimulatorScreen
        _screen = SimulatorScreen()
    else:
        from c4_sign.lib.screen.matrix import MatrixScreen
        _screen = MatrixScreen()
    _screen_manager.update_tasks()

def screen_active():
    now = arrow.now()
    # normal hours! between 6 am and midnight.
    return now.hour >= 6 and now.hour < 24

def update_screen():
    global _screen, _last_update, _screen_manager
    
    now = arrow.now()
    delta_t = now - _last_update
    _last_update = now
    
    # clear canvas
    canvas = Canvas()

    # brightness
    if screen_active():
        _screen.brightness = 100
    else:
        _screen.brightness = 0
        _screen.update_display(canvas)
        return # don't draw anything!

    # draw stuff
    try:
        _screen_manager.draw(canvas, delta_t)
    except Exception as e:
        print("ERROR: ", e)
        print("Traceback:" + "".join(traceback.format_tb(e.__traceback__)))
        print(e.__traceback__.tb_frame.f_code.co_filename, e.__traceback__.tb_lineno)
        _screen_manager.override_current_task(ErrorScreenTask(e))
    
    _screen.update_display(canvas)
