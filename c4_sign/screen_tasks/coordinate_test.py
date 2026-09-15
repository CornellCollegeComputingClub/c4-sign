from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.lib.canvas import Canvas


class CoordinateTest(ScreenTask):
    canonical_name = "CoordinateTest"
    title = "CoordTest"
    artist = "Mac Coleman"
    description = "A basic task to test whether the coordinates of the sign are correct. " \
        "The red component increases from left to right, and green from top to bottom."
    ignore = True

    def prepare(self):
        return super().prepare()

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:
        for y in range(32):
            for x in range(32):
                canvas.set_pixel(x, y, (int(x / 32 * 255), int(y / 32 * 255), 0))

        if self.elapsed_time > self.suggested_run_time:
            return True
        else:
            return False
