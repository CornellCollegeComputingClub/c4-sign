import math
from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.lib.canvas import Canvas
from c4_sign.lib.graphics import fill_screen


class RainbowWave(ScreenTask):
    title = "Rainbow Wave"
    artist = "Mac Coleman"

    def prepare(self):
        self.frame = 0
        self.epic_colors = [
            0xFF0000,
            0xFF6000,
            0xFFBF00,
            0xB5FF00,
            0x80FF00,
            0x20FF00,
            0x00FF40,
            0x00FFFF,
            0x009FFF,
            0x0040FF,
            0x2000FF,
            0x7F00FF,
            0xDF00FF,
            0xFF00BF,
            0xFF0060,
        ]
        return super().prepare()

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:

        for x in range(32):
            for y in range(32):
                color = self.epic_colors[
                    (int(math.sqrt((15.5 - x) ** 2 + (15.5 - y) ** 2) - self.frame)) % len(self.epic_colors)
                ]
                canvas.set_pixel(x, y, color)
        self.frame += 1

        if self.elapsed_time > self.suggested_run_time:
            return True
        else:
            return False
