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
        error_name = type(self.error).__name__ + " " * 5
        error_name_width = sum([FONT_4x6.character_width(ord(c)) or FONT_4x6.character_width(ord("a")) for c in error_name])
        # marquee!
        if error_name_width > 32:
            e_offset = int(self.elapsed_time.total_seconds() * 10) % error_name_width
            # speedup at the end so we can pause at the start!
            if e_offset > error_name_width - 32:
                e_offset = 0
            graphics.draw_text(canvas, FONT_4x6, 1 - e_offset, 14, COLOR_RED, error_name)
            graphics.draw_text(canvas, FONT_4x6, error_name_width - e_offset, 14, COLOR_RED, error_name)
        else:
            graphics.draw_text(canvas, FONT_4x6, 1, 14, COLOR_RED, error_name)
        msg = str(self.error) + " " * 5
        msg_width = sum([FONT_4x6.character_width(ord(c)) or FONT_4x6.character_width(ord("a")) for c in msg])
        # marquee!
        if msg_width > 32:
            offset = int(self.elapsed_time.total_seconds() * 10) % msg_width
            # speedup at the end so we can pause at the start!
            if offset > msg_width - 32:
                offset = 0
            graphics.draw_text(canvas, FONT_4x6, 1 - offset, 21, COLOR_RED, msg)
            graphics.draw_text(canvas, FONT_4x6, msg_width - offset, 21, COLOR_RED, msg)
        else:
            graphics.draw_text(canvas, FONT_4x6, 1, 21, COLOR_RED, msg)
        return offset == 0 and e_offset == 0

    def get_lcd_text(self) -> str:
        return str(self.error).ljust(32)
