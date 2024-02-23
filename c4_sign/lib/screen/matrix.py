from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
import neopixel
import board

class MatrixScreen(ScreenBase):
    def __init__(self):
        self.__pixels = neopixel.NeoPixel(board.D18, 32*32, brightness=0.05, auto_write=False)

    def update_display(self, canvas: Canvas):
        self.__pixels[::1] = canvas.tolist()
        self.__pixels.show()
    
    def update_lcd(self, text):
        pass
        # return super().update_lcd(text)
