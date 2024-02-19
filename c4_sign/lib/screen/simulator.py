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
            print("\033[0G", end="")  # Move cursor to 0,0
            print("\033[0d", end="")
            print("\033[2J", end="")  # Clear screen
            canvas.debug()
            sleep(1/24)
        except KeyboardInterrupt:
            print("\033[?1049l", end="")  # Disable alternate buffer
            sys.exit(0)
