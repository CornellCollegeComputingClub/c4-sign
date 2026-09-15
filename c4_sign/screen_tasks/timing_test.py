from c4_sign.base_task import ScreenTask

import math
from datetime import timedelta
from c4_sign.lib.canvas import Canvas

from c4_sign.lib.graphics import fill_screen

class TimingTest(ScreenTask):
    canonical_name = "TimingTest"
    title = "Timing Test"
    artist = "Mac Coleman"
    description = "A task originally meant to test timing of the sign and make sure that it could draw colors at a full 24 FPS."
    ignore = True

    def prepare(self):
        self.colors = [
            0x00FFFF,
            0xFF00FF,
            0xFFFF00,
        ]
        return super().prepare()

    def draw_frame(self, canvas: Canvas, deltaTime: timedelta) -> bool:
        i = math.floor(self.elapsed_time.total_seconds() * 0.5) % 3
        fill_screen(canvas, self.colors[i])
        return False
