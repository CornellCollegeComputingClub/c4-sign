from c4_sign.base_task import ScreenTask

import math
from datetime import timedelta
from c4_sign.lib.canvas import Canvas

from c4_sign.lib.graphics import fill_screen

class ColorTest(ScreenTask):
    title = "Timing Test"
    artist = "Mac Coleman"

    def prepare(self):
        self.colors = [
            0x00FFFF,
            0xFF00FF,
            0xFFFF00,
        ]

    def draw_frame(self, canvas: Canvas, deltaTime: timedelta) -> bool:
        i = math.floor(self.elapsed_time.total_seconds() * 0.5) % 3
        fill_screen(canvas, self.colors[i])
        return False
