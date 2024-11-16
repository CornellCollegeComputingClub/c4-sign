from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import video_to_images

from datetime import timedelta
from PIL import Image
import numpy

class StickFight(ScreenTask):
    title = "Stick Fight"
    artist = "Aaron Standefer"
    
    def __init__(self):
        super().__init__(timedelta(seconds=1), timedelta(hours=1))
        self.prepare_stick_fight()
    
    def prepare_stick_fight(self):
        image_folder_path = video_to_images("https://www.youtube.com/watch?v=p4F61wWMgLY")
        self.image_folder_path = image_folder_path
        
    def prepare(self):
        self.stop = False
        self.frame = 1
        super().prepare()
        return True
    
    def draw_frame(self, canvas, delta_time):
        image = Image.open(self.image_folder_path / f"{self.frame}.png")
        graphics.draw_image(canvas, 0, 0, numpy.array(image))
        self.frame += 1
        if self.frame > 1153:
            self.frame = 1
            self.stop = True
        return self.stop