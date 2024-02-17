from datetime import timedelta
from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_RED, FONT_4x6

# meta, i know!
class ErrorScreenTask(ScreenTask):
    ignore = True
    def __init__(self, error: Exception):
        super().__init__(timedelta(seconds=10), timedelta(minutes=1))
        self.error = error
    
    def draw_frame(self, canvas, delta_time):
        return
        graphics.DrawText(canvas, FONT_4x6, 1, 7, COLOR_RED, "Error :(")
        graphics.DrawText(canvas, FONT_4x6, 1, 14, COLOR_RED, type(self.error).__name__)
        msg = str(self.error) + " " * 10
        width = sum([FONT_4x6.CharacterWidth(ord(c)) or FONT_4x6.CharacterWidth(ord("a")) for c in msg])
        # marquee!
        if width > 64:
            offset = int(self.elapsed_time.total_seconds() * 10) % width
            # speedup at the end so we can pause at the start!
            if offset > width - 32:
                offset = 0
            graphics.DrawText(canvas, FONT_4x6, 1 - offset, 21, COLOR_RED, msg)
            graphics.DrawText(canvas, FONT_4x6, width - offset, 21, COLOR_RED, msg)
        else:
            graphics.DrawText(canvas, FONT_4x6, 1, 21, COLOR_RED, msg)

    @classmethod
    def construct_from_config(cls, config):
        return cls(config['error'])