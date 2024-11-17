
import arrow

from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_TEAL, FONT_PICO
from c4_sign.lib import graphics


class Uptime(ScreenTask):
    title = "Uptime"
    artist = "Luna"

    def __init__(self):
        super().__init__()
        self.sign_started = arrow.now()

    def prepare(self):
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        now = arrow.now()
        uptime = now - self.sign_started
        uptime_str = str(uptime).split(".")[0]
        graphics.draw_text(canvas, FONT_PICO, 1, 6, COLOR_TEAL, uptime_str)
