from c4_sign.lib.screen.base import ScreenBase
from time import sleep
import sys


class SimulatorScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        print("\033[?1049h", end="")  # Enable alternate buffer
    
    def update_lcd(self, text):
        print(text)
    
    def update_display(self, canvas):
        try:
            canvas.debug()
            sleep(1/24)
        except KeyboardInterrupt:
            print("\033[?1049l", end="")  # Disable alternate buffer
            sys.exit(0)
