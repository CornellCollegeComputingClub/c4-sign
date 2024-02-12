from datetime import timedelta
import random
from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_CYAN, COLOR_WHITE, FONT_4x6, FONT_5x7

class Slogan(ScreenTask):
    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        self.slogan = random.choices([
            "Foster Home of Rock & Roll",
            "Unoffical Weezer Fan Club",
            "We Still Exist!"
        ], weights=[0.90, 0.05, 0.05])[0]
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        self.draw_header(canvas)
        msg = str(self.slogan) + " " * 10
        width = sum([FONT_4x6.CharacterWidth(ord(c)) or FONT_4x6.CharacterWidth(ord("a")) for c in msg])

        graphics.DrawText(canvas, FONT_5x7, 1, 15, COLOR_CYAN, " KRNL Radio")

        if (width - FONT_4x6.CharacterWidth(ord(" ")) * 10) > 64:
            offset = int(self.elapsed_time.total_seconds() * 10) % width
            # speedup at the end so we can pause at the start!
            if offset > width - 32:
                offset = 0
            graphics.DrawText(canvas, FONT_4x6, 1 - offset, 24, COLOR_WHITE, msg)
            graphics.DrawText(canvas, FONT_4x6, width - offset, 24, COLOR_WHITE, msg)
        else:
            graphics.DrawText(canvas, FONT_4x6, 1, 24, COLOR_WHITE, msg.strip().center(16))
        # graphics.DrawText(canvas, FONT_4x6, 1, 15, COLOR_WHITE, self.slogan.center(16))
    
    @classmethod
    def construct_from_config(cls, config):
        return cls()
