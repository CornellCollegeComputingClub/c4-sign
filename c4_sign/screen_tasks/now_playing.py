import random
from datetime import timedelta
from c4_sign.base_task import ScreenTask
import c4_sign.lib.graphics.graphics as graphics

class KRNLNowPlaying(ScreenTask):
    def prepare(self):
        self.frame = 0
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        r, g, b = self.frame, 0, 255 - self.frame
        graphics.fill_screen(canvas, (r, g, b))
        self.frame += 4 % 255