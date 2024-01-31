from time import sleep
import traceback
import arrow
from c4_sign.ScreenManager import ScreenManager
from c4_sign.consts import COLOR_RED, COLOR_WHITE, FONT_4x6, FONT_5x7

from c4_sign.screen_tasks.error import ErrorScreenTask
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

_matrix = None
_canvas = None
_lcd = None
_screen_manager = ScreenManager()
_frame_count = 0
_last_update = arrow.now()


def init_matrix():
    global _matrix, _canvas, _lcd
    options = RGBMatrixOptions()
    # 4 separate panels, TODO: figure out THAT.
    options.rows = 64
    options.cols = 64
    options.disable_hardware_pulsing = True
    # options.gpio_slowdown = ???
    _matrix = RGBMatrix(options = options)
    _canvas = _matrix.CreateFrameCanvas()
    # lcd is 2col x 16char
    _lcd = None # TODO: this!
    _screen_manager.update_tasks()

def clear_matrix():
    global _matrix
    if _matrix is not None:
        _matrix.Clear()

def draw_headline_and_msg(canvas, headline, msg, headline_bg_color, msg_color, headline_fg_color=COLOR_WHITE, MSG_FONT=FONT_5x7, HEADLINE_FONT=FONT_5x7):
    headline_width = sum([HEADLINE_FONT.CharacterWidth(ord(c)) or HEADLINE_FONT.CharacterWidth(ord("a")) for c in headline])
    msg_width = sum([MSG_FONT.CharacterWidth(ord(c)) or MSG_FONT.CharacterWidth(ord("a")) for c in msg])
    if headline_width > 64 or msg_width > 64:
        print("ERROR: text too long")
        return draw_headline_and_msg(canvas, "Sign Error", "Text too long", None, COLOR_WHITE, COLOR_RED, FONT_4x6)
    headline_x = 32 - (headline_width // 2)
    msg_x = 32 - (msg_width // 2)
    if headline_bg_color:
        draw_rect(canvas, headline_x - 1, 10, headline_width + 1, HEADLINE_FONT.height + 1, headline_bg_color)
    graphics.DrawText(canvas, HEADLINE_FONT, headline_x, 17, headline_fg_color, headline)
    graphics.DrawText(canvas, MSG_FONT, msg_x, 27, msg_color, msg)

def draw_progress(canvas, progress, color=COLOR_RED):
    draw_rect(canvas, 1, 13, 62, 6, COLOR_WHITE, False)
    progress = max(0, min(1, progress))
    if progress > 0:
        draw_rect(canvas, 2, 14, int(60 * progress), 4, color, True)

def draw_spinner(canvas, spinner, frame_counter=0, color=COLOR_RED):
    font = FONT_5x7
    spinner_frame = spinner["frames"][frame_counter % len(spinner["frames"])]
    spinner_delay = spinner["interval"] / 1000
    # print(spinner_frame, ord(spinner_frame))
    spinner_width = sum([font.CharacterWidth(ord(c)) or font.CharacterWidth(ord('a')) for c in spinner_frame])
    spinner_x = 32 - (spinner_width // 2)
    graphics.DrawText(canvas, font, spinner_x, 16, color, spinner_frame)
    sleep(spinner_delay)

def draw_rect(canvas, x, y, w, h, color, fill=True):
    # use Canvas.SetPixel() to fill
    if fill:
        for i in range(h):
            graphics.DrawLine(canvas, x, y + i, x + w - 1, y + i, color)
    else:
        graphics.DrawLine(canvas, x, y, x + w - 1, y, color)
        graphics.DrawLine(canvas, x, y, x, y + h - 1, color)
        graphics.DrawLine(canvas, x + w - 1, y, x + w - 1, y + h - 1, color)
        graphics.DrawLine(canvas, x, y + h - 1, x + w - 1, y + h - 1, color)

def screen_active():
    now = arrow.now()
    if is_summer():
        # summer time! between 6 am and 8 pm.
        return now.hour >= 6 and now.hour < 20
    else:
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
        # draw_headline_and_msg(canvas, "Sign Error", "No internet!", COLOR_RED, COLOR_WHITE, COLOR_RED, FONT_4x6)
    
    # update the screen~
    _canvas = _matrix.SwapOnVSync(canvas)

