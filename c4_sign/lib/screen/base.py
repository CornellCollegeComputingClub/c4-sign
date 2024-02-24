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
