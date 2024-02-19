import random
from datetime import timedelta
from c4_sign.base_task import ScreenTask
import c4_sign.lib.graphics.graphics as graphics

class KRNLNowPlaying(ScreenTask):
    def prepare(self):
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        r, g, b = [random.randint(0,255) for x in range(3)]
        graphics.fill_screen(canvas, (r, g, b))