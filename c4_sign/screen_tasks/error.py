from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_RED, FONT_4x6
from c4_sign.lib import graphics


# this is still not quite working yet...
# meta, i know!
class ErrorScreenTask(ScreenTask):
    ignore = True

    def __init__(self, error: Exception):
        super().__init__(timedelta(seconds=10), timedelta(minutes=1))
        self.error = error

    def draw_frame(self, canvas, delta_time):
        graphics.draw_text(canvas, FONT_4x6, 1, 7, COLOR_RED, "Error :(")
        graphics.draw_text(canvas, FONT_4x6, 1, 14, COLOR_RED, type(self.error).__name__)
        msg = str(self.error) + " " * 10
        width = sum([FONT_4x6.character_width(ord(c)) or FONT_4x6.character_width(ord("a")) for c in msg])
        # marquee!
        # if width > 32:
        #     offset = int(self.elapsed_time.total_seconds() * 10) % width
        #     # speedup at the end so we can pause at the start!
        #     if offset > width - 32:
        #         offset = 0
        #     graphics.draw_text(canvas, FONT_4x6, 1 - offset, 21, COLOR_RED, msg)
        #     graphics.draw_text(canvas, FONT_4x6, width - offset, 21, COLOR_RED, msg)
        # else:
        graphics.draw_text(canvas, FONT_4x6, 1, 21, COLOR_RED, msg)

    def get_lcd_text(self) -> str:
        return self.error
