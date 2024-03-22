from typing import Sequence, Union

import board
import digitalio
from neopixel_write import neopixel_write

from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.physical.driver import lcd


class NeoPixel:
    def __init__(self, pin, num_pixels, brightness=1.0, auto_write=True):
        self.buf = bytearray(3 * num_pixels)
        self._nums = num_pixels
        self.brighness = brightness
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.auto_write = auto_write

    def __setitem__(self, index: Union[int, slice], val: Union[tuple[int, int, int], Sequence[tuple[int, int, int]]]):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._nums)
            for val, in_val in enumerate(range(start, stop, step)):
                self._set_item(in_val, val)
        else:
            self._set_item(index, val)

        if self.auto_write:
            self.show()

    def _set_item(self, index, val: tuple[int, int, int]):
        # val = (r, g, b)
        # neopixels use GRB
        if index < 0:
            index += len(self)
        if index >= self._nums or index < 0:
            raise IndexError
        offset = index * 3
        self.buf[offset] = val[1]  # green
        self.buf[offset + 1] = val[0]  # red
        self.buf[offset + 2] = val[2]  # blue

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self._get_item(i) for i in range(*index.indices(self._nums))]
        else:
            return self._get_item(index)

    def _get_item(self, index):
        offset = index * 3
        return self.buf[offset + 1], self.buf[offset], self.buf[offset + 2]  # GRB -> RGB

    def show(self):
        if self.brighness < 1.0:
            # apply brightness
            buf = bytearray(len(self.buf))
            for i, val in enumerate(self.buf):
                buf[i] = int(val * self.brighness)
            self._transmit(buf)
        else:
            self._transmit(self.buf)

    def _transmit(self, buf):
        neopixel_write(self.pin, buf)


class MatrixScreen(ScreenBase):
    def __init__(self):
        self.__pixels = NeoPixel(board.D18, 32 * 32, brightness=0.05, auto_write=False)
        self.__lcd = lcd()
        self.__cached_text = " " * 32
        self.loading_screen()

    def update_display(self, canvas: Canvas):
        # for i in range(32*32):
        #     self.__pixels[i] = canvas[i]
        x = lambda i: self.__pixels.__setitem__(i, canvas[i])
        [x(i) for i in range(32 * 32)]
        self.__pixels.show()

    def update_lcd(self, text):
        if text == self.__cached_text:
            return
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string(text[:16], 1)
        self.__lcd.lcd_display_string(text[16:], 2)
        self.__cached_text = text
