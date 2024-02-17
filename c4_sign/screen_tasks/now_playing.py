from datetime import timedelta
from c4_sign.base_task import ScreenTask
import c4_sign.lib.graphics.graphics as graphics

class KRNLNowPlaying(ScreenTask):
    def prepare(self):
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        graphics.fill_screen(canvas, (255, 0, 255))