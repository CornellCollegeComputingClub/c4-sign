from datetime import timedelta
from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_GRAY, COLOR_WHITE, FONT_4x6, FONT_5x7


class KRNLNowPlaying(ScreenTask):
    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=30), max_run_time=timedelta(seconds=60))
    
    def prepare(self):
        self.track_data = get_current_track()
        self.did_once = False
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        self.draw_header(canvas)
        msg = str(self.track_data['title']) + " " * 10
        width = sum([FONT_4x6.CharacterWidth(ord(c)) or FONT_4x6.CharacterWidth(ord("a")) for c in msg])

        graphics.DrawText(canvas, FONT_5x7, 1, 15, COLOR_GRAY, " NOW PLAYING")

        if (width - FONT_4x6.CharacterWidth(ord(" ")) * 10) > 64:
            offset = int(self.elapsed_time.total_seconds() * 10) % width
            # speedup at the end so we can pause at the start!
            if offset > width - 32:
                offset = 0
                self.did_once = True
            graphics.DrawText(canvas, FONT_4x6, 1 - offset, 24, COLOR_WHITE, msg)
            graphics.DrawText(canvas, FONT_4x6, width - offset, 24, COLOR_WHITE, msg)
        else:
            graphics.DrawText(canvas, FONT_4x6, 1, 24, COLOR_WHITE, msg.strip().center(16))
        
        return self.did_once
        # graphics.DrawText(canvas, FONT_4x6, 1, 15, COLOR_WHITE, self.slogan.center(16))
    
    @classmethod
    def construct_from_config(cls, config):
        return cls()