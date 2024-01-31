from time import sleep
import traceback
import arrow
from c4_sign.ScreenManager import ScreenManager
from c4_sign.consts import COLOR_RED, COLOR_WHITE, FONT_4x6, FONT_5x7

from c4_sign.screen_tasks.error import ErrorScreenTask
_neopixels = None
_lcd = None
_screen_manager = ScreenManager()
_frame_count = 0
_last_update = arrow.now()


def init_matrix():
    global _neopixels, _lcd
    # 4 separate panels, TODO: figure out THAT.
    _neopixels = None # TODO: this!
    # lcd is 2col x 16char
    _lcd = None # TODO: this!
    _screen_manager.update_tasks()

def clear_matrix():
    global _matrix
    if _matrix is not None:
        _matrix.Clear()

def screen_active():
    now = arrow.now()
    # normal hours! between 6 am and midnight.
    return now.hour >= 6 and now.hour < 24

def blank_screen():
    global _matrix, _canvas
    canvas = _canvas
    canvas.Clear()
    _canvas = _matrix.SwapOnVSync(canvas)

def update_screen():
    global _matrix, _canvas, _last_update, _screen_manager
    
    now = arrow.now()
    delta_t = now - _last_update
    _last_update = now
    
    # clear canvas
    canvas = _canvas
    canvas.Clear()

    # brightness
    if screen_active():
        _matrix.brightness = 100
    else:
        _matrix.brightness = 0
        _canvas = _matrix.SwapOnVSync(canvas)
        return # don't draw anything!

    # draw stuff
    try:
        _screen_manager.draw(canvas, delta_t)
    except Exception as e:
        print("ERROR: ", e)
        print("Traceback:" + "".join(traceback.format_tb(e.__traceback__)))
        print(e.__traceback__.tb_frame.f_code.co_filename, e.__traceback__.tb_lineno)
        _screen_manager.override_current_task(ErrorScreenTask(e))
    
    # update the screen~
    _canvas = _matrix.SwapOnVSync(canvas)

