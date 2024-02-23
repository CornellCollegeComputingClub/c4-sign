from c4_sign.lib.screen.base import ScreenBase
from time import sleep
import sys


class SimulatorScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        self.text = ""
        print("\033[?1049h", end="")  # Enable alternate buffer
    
    def update_lcd(self, text):
        self.text = text
    
    def update_display(self, canvas):
        return
        try:
            print("\033[0G", end="")  # Move cursor to 0,0
            print("\033[0d", end="")
            print("\033[2J", end="")  # Clear screen
            print("\033[?25l", end="")  # Hide cursor
            print(self.text)
            canvas.debug()
            sleep(1/24)
        except KeyboardInterrupt:  # Should relocate this...
            print("\033[?1049l", end="")  # Disable alternate buffer
            print("\033[?25h", end="")  # Show cursor
            sys.exit(0)
