import numpy
from PIL import Image

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import video_to_images


class BadApple(ScreenTask):
    def __init__(self):
        super().__init__()
        self.prepare_bad_apple()

    def prepare_bad_apple(self):
        # this'll take a bit...
        # first, we need to load the video and split it into frames
        # then we need to convert each frame into a 32x32 image
        # ...yeah. fortunately, we can cache this!
        image_folder_path = video_to_images("https://www.youtube.com/watch?v=FtutLA63Cp8")
        self.image_folder_path = image_folder_path

    def prepare(self):
        self.frame = 1
        return True

    def get_lcd_text(self) -> str:
        return "bad apple".ljust(32)

    def draw_frame(self, canvas, delta_time):
        # we need to load the image
        image = Image.open(self.image_folder_path / f"{self.frame}.png")
        image = image.resize((32, 32))
        graphics.draw_image(canvas, 0, 0, numpy.array(image))
        self.frame += 1
        if self.frame > 5258:
            self.frame = 1
        return True
