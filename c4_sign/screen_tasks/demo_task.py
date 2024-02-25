import random
from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics


class Demo(ScreenTask):
    title = "Demo"
    artist = "Mac Coleman"

    def prepare(self):
        self.frame = 0
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        r, g, b = self.frame, 0, 255 - self.frame
        graphics.fill_screen(canvas, (r, g, b))
        self.frame = (self.frame + 4) % 255

        if self.elapsed_time > self.suggested_run_time:
            return True
        else:
            return False
