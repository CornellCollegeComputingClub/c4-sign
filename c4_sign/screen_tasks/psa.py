from datetime import timedelta
import arrow
import requests
import random
import json
import segno
import io
from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_CYAN, COLOR_PURPLE, COLOR_WHITE, DEV_MODE, FONT_4x6, FONT_5x7, FONT_9x15
from c4_sign.util import requests_get_1hr_cache
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

class RandomPSA(ScreenTask):
    psa: dict

    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        req = requests_get_1hr_cache("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/psa.json")
        self.psa = random.choice(req.json()['contents'])
        return super().prepare() and self.prepare_qr_code()
    
    def prepare_qr_code(self):
        if self.psa['type'] == 'qr':
            self.suggested_run_time = timedelta(seconds=30) # can we do this dynamically?
            qr_code = segno.make_qr(self.psa['data'])
            buf = io.StringIO()
            qr_code.save(buf, kind='txt', border=0)
            self.qr_code = buf.getvalue().splitlines()
            if len(self.qr_code) > 25:
                print("QR code too big!")
                return False
        else:
            return False
        return True

    def draw_frame(self, canvas, delta_time):
        if not self.psa['type'] == 'qr':
            self.draw_header(canvas)
            graphics.DrawText(canvas, FONT_4x6, 1, 15, COLOR_WHITE, self.psa['text'].center(16))
        else:
            now = arrow.now()
            current_time = now.format("h:mm").rjust(5)
            graphics.DrawText(canvas, FONT_4x6, 1, 32, COLOR_PURPLE, current_time)
            graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_WHITE, self.psa['text'].center(16))
            current_line = 7
            for line in self.qr_code:
                current_x = 20
                for char in line:
                    if char == '0':
                        canvas.SetPixel(current_x, current_line, 255, 255, 255)
                    else:
                        canvas.SetPixel(current_x, current_line, 0, 0, 0)
                    current_x += 1
                current_line += 1

    @classmethod
    def construct_from_config(cls, config):
        return cls()

class SelectPSA(RandomPSA):
    def __init__(self, psa_key: str):
        super().__init__()
        self.psa_key = psa_key
    
    def prepare(self):
        req = requests_get_1hr_cache("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/psa.json")
        psas = req.json()['contents']
        for psa in psas:
            if psa['key'] == self.psa_key:
                self.psa = psa
                break
        if not self.psa:
            print("PSA not found!")
            return False
        return super().prepare() and self.prepare_qr_code()
    
    @classmethod
    def construct_from_config(cls, config):
        return cls(config['key'])

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

class ShowsAndCounting(ScreenTask):
    # literally just for tabling lol
    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        self.shows = "10"
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        self.draw_header(canvas)
        graphics.DrawText(canvas, FONT_9x15, 23, 20, COLOR_CYAN, self.shows)
        graphics.DrawText(canvas, FONT_4x6, 1, 30, COLOR_WHITE, "Shows & Counting")
    
    @classmethod
    def construct_from_config(cls, config):
        return cls()

class Relics(ScreenTask):
    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        return super().prepare()
    
    def draw_frame(self, canvas, delta_time):
        graphics.DrawText(canvas, FONT_9x15, 5, 16, COLOR_WHITE, "Relics")
        graphics.DrawText(canvas, FONT_4x6, 0, 25, COLOR_CYAN, "Thurs. 8-10pm".center(16))
        # graphics.DrawText(canvas, FONT_4x6, 1, 30, COLOR_CYAN, "krnl-radio.github.io")
    
    @classmethod
    def construct_from_config(cls, config):
        return cls()