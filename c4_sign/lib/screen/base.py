from abc import ABC, abstractmethod

class ScreenBase(ABC):
    def __init__(self):
        self.brightness = 100
    
    @abstractmethod
    def update_lcd(self, text):
        pass

    @abstractmethod
    def update_display(self, canvas):
        pass
