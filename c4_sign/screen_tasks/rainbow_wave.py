import math
from datetime import timedelta

from c4_sign.base_task import OptimScreenTask
from c4_sign.lib.canvas import Canvas


class RainbowWave(OptimScreenTask):
    canonical_name = "RainbowWave"
    title = "Rainbow Wave"
    artist = "Mac Coleman"
    description = "Displays a wave of rainbow colors emanating from the center of the screen. " \
    "The colors are chosen from a list of 16 colors. Each pixel is assigned a color based on " \
    "its distance from the center, and each frame the color associated with each distance is " \
    "shifted over to make the colors propagate from the center."

    def prepare(self):
        self.frame = 0
        self.epic_colors = [
            0xFF0000,
            0xFF6200,
            0xFFBF00,
            0xDDFF00,
            0x80FF00,
            0x1EFF00,
            0x00FF40,
            0x00FFA2,
            0x00FFFF,
            0x009DFF,
            0x0040FF,
            0x2200FF,
            0x8000FF,
            0xE100FF,
            0xFF00BF,
            0xFF005D,
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
