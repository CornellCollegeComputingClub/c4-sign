from c4_sign.lib.screen.base import ScreenBase
from time import sleep

class SimulatorScreen(ScreenBase):
    def __init__(self):
        super().__init__()
    
    def update_lcd(self, text):
        print(text)
    
    def update_display(self, canvas):
        canvas.debug()
        sleep(1/24)