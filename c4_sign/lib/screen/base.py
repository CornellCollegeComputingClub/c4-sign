from abc import ABC, abstractmethod

from c4_sign.lib.canvas import Canvas


class ScreenBase(ABC):
    def __init__(self):
        self.brightness = 100

    @abstractmethod
    def update_lcd(self, text: str):
        pass

    @abstractmethod
    def update_display(self, canvas: Canvas):
        pass

    def debug_info(self, **kwargs):
        pass

    def debug_override(self, screen_manager):
        pass

    def loading_screen(self):
        from time import sleep
        from c4_sign.lib.graphics import draw_text
        from c4_sign.consts import FONT_PICO, COLOR_WHITE

        sleep(1)  # wait for things to finish setting up so we can draw
        self.update_lcd("Loading...".ljust(32))
        c = Canvas()
        draw_text(c, FONT_PICO, 1, 6, COLOR_WHITE, ">Load")
        self.update_display(c)

    def loading_cb(self, text):
        from c4_sign.lib.graphics import draw_text
        from c4_sign.consts import FONT_PICO, COLOR_GRAY, COLOR_WHITE

        self.update_lcd("Loading...".ljust(16) + text.ljust(16))
        c = Canvas()
        draw_text(c, FONT_PICO, 1, 6, COLOR_WHITE, ">Load")
        draw_text(c, FONT_PICO, 1, 12, COLOR_GRAY, text)
        self.update_display(c)
