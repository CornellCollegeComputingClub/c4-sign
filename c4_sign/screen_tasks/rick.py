import random
from datetime import timedelta

import numpy
import srt
from PIL import Image

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import file_from_google_drive, video_to_images


class RickRoll(ScreenTask):
    title = "Rick Roll"
    artist = "Luna"

    def __init__(self):
        super().__init__(timedelta(seconds=1), timedelta(hours=1))  # :)
        self.prepare_rick()

    def prepare_rick(self):
        # this'll take a bit...
        # first, we need to load the video and split it into frames
        # then we need to convert each frame into a 32x32 image
        # ...yeah. fortunately, we can cache this!
        image_folder_path = video_to_images("https://www.youtube.com/watch?v=fH64whs5tzI")
        self.image_folder_path = image_folder_path
        subs = file_from_google_drive("rick.srt")
        with subs.open() as f:
            self.subtitles = list(srt.parse(f.read()))

    def prepare(self):
        # weighted random choice, we want a 2% chance of the full video
        self.stop = False
        self.frame = 1
        return random.random() < 0.02

    def get_lcd_text(self) -> str:
        current_time = self.frame * (1 / 24)
        for subtitle in self.subtitles:
            if subtitle.start.total_seconds() < current_time < subtitle.end.total_seconds():
                content = subtitle.content.ljust(32)
                if len(content) > 32:
                    # add ... to the end
                    content = content[:29] + "..."
                return content
        return super().get_lcd_text()

    def draw_frame(self, canvas, delta_time):
        # we need to load the image
        image = Image.open(self.image_folder_path / f"{self.frame}.png")
        graphics.draw_image(canvas, 0, 0, numpy.array(image))
        self.frame += 1
        if self.frame > 5088:
            self.frame = 1
            self.stop = True
        return self.stop
