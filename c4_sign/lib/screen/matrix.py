from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.physical.driver import lcd
import neopixel
import board

class MatrixScreen(ScreenBase):
    def __init__(self):
        self.__pixels = neopixel.NeoPixel(board.D18, 32*32, brightness=0.05, auto_write=False)
        self.__lcd = lcd()
        self.__cached_text = " " * 32

    def update_display(self, canvas: Canvas):
        # for i in range(32*32):
        #     self.__pixels[i] = canvas[i]
        x = lambda i: self.__pixels.__setitem__(i, canvas[i])
        [x(i) for i in range(32*32)]
        self.__pixels.show()
    
    def update_lcd(self, text):
        if text == self.__cached_text:
            return
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string(text[:16], 1)
        self.__lcd.lcd_display_string(text[16:], 2)
        self.__cached_text = text
        # return super().update_lcd(text)
