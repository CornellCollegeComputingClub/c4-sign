import random
from datetime import timedelta

import c4_sign.lib.graphics.graphics as graphics
from c4_sign.base_task import ScreenTask


class KRNLNowPlaying(ScreenTask):
    def prepare(self):
        self.frame = 0
        return super().prepare()

    def get_lcd_text(self) -> str:
        return "hello world!".ljust(32)

    def draw_frame(self, canvas, delta_time):
        r, g, b = self.frame, 0, 255 - self.frame
        graphics.fill_screen(canvas, (r, g, b))
        self.frame = (self.frame + 4) % 255
