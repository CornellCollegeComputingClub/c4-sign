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

        sleep(1)  # wait for things to finish setting up so we can draw
        self.update_lcd("Loading...".ljust(32))
        c = Canvas()
        self.update_display(c)

    def loading_cb(self, text):
        self.update_lcd("Loading...".ljust(16) + text.ljust(16))
        c = Canvas()
        self.update_display(c)
