from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import file_from_google_drive, video_to_images
from c4_sign.lib.canvas import Canvas

from c4_sign.consts import MOTD_TEXT, FONT_9x15, FONT_5x7, COLOR_PURPLE, COLOR_WHITE

from PIL import Image
from numpy import array


class ExplosionMOTD(ScreenTask):
    title = "Explosion!"
    artist = "Mac Coleman"

    def __init__(self):
        super().__init__(timedelta(seconds=1), timedelta(hours=1))
        self.prepare_explosion_motd()



    def prepare_explosion_motd(self):
        self.__image_folder_path = file_from_google_drive("explosion")

    def prepare(self):
        self.__title_format_string = "explosion{:02d}.png"
        self.__frame = 0
        self.__frame_count = 17
        self.__wait_frames = 20
        self.__offset = 0
        self.__message = " ".join(MOTD_TEXT for _ in range(1))
        self.__length = self.__frame_count + self.__wait_frames + len(self.__message) * 5 + 20
        self.__reverse_frame = 0
    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:

        if self.__frame > 9:
            graphics.draw_text(canvas, FONT_9x15, self.__offset + 7, 22, COLOR_PURPLE, "C4")
        graphics.draw_text(canvas, FONT_9x15, self.__offset - 2, 22, COLOR_WHITE, "<  >")
        graphics.draw_text(canvas, FONT_5x7, self.__offset + 35, 20, COLOR_WHITE, self.__message)

        if self.__frame_count - self.__reverse_frame > 9:
            graphics.draw_text(canvas, FONT_9x15, self.__offset + self.__length + 7, 22, COLOR_PURPLE, "C4")

        draw_image = False
        reverse = False

        if self.__frame < self.__frame_count:
            draw_image = True
        elif self.__frame > self.__frame_count + self.__wait_frames and abs(self.__offset) < self.__length:
            self.__offset -= 1
        elif self.__frame > self.__frame_count + self.__wait_frames * 2:
            draw_image = True
            reverse = True

        if draw_image:
            index = max(1, self.__frame_count - self.__reverse_frame) if reverse else self.__frame + 1
            if reverse:
                self.__reverse_frame += 1
            img = Image.open(self.__image_folder_path / self.__title_format_string.format(index)).convert(
                "RGBA")
            graphics.draw_image(canvas, 0, 0, array(img))

            if index == 1 and reverse:
                return True

        self.__frame += 1