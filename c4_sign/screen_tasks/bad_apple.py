import random
from datetime import timedelta

import numpy
import srt
from PIL import Image

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import file_from_url, video_to_images


class BadApple(ScreenTask):
    title = "Bad Apple!!"
    artist = "Luna"
    sections = [
        range(1, 1011),
        range(1011, 2211),
        range(2211, 2661),
        range(2661, 3363),
        range(3363, 4349),
        range(4349, 5259),
    ]

    def __init__(self):
        super().__init__(timedelta(seconds=1), timedelta(hours=1))  # :)
        self.prepare_bad_apple()

    def prepare_bad_apple(self):
        # this'll take a bit...
        # first, we need to load the video and split it into frames
        # then we need to convert each frame into a 32x32 image
        # ...yeah. fortunately, we can cache this!
        image_folder_path = video_to_images("https://www.youtube.com/watch?v=FtutLA63Cp8")
        # image_folder_path = video_to_images("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.image_folder_path = image_folder_path
        subs = file_from_url("https://archive.org/download/bad-apple-resources/subs/bad_apple_ja-rom.srt")
        with subs.open() as f:
            self.subtitles = list(srt.parse(f.read()))

    def prepare(self):
        # weighted random choice, we want a 2% chance of the full video
        if random.random() < 0.02:
            self.section = range(1, 5259)
            print("full video!")
        else:
            self.section = random.choice(self.sections)
        self.frame = self.section.start
        self.stop = False
        return True

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
        if self.frame > 5258:
            self.frame = 1
            self.stop = True
        return self.frame > self.section.stop or self.stop
