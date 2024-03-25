from typing import Sequence, Union

import digitalio
from neopixel_write import neopixel_write


class NeoPixel:
    def __init__(self, pin, num_pixels, brightness=1.0, auto_write=True):
        self.buf = bytearray(3 * num_pixels)
        self._nums = num_pixels
        self.brightness = brightness
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.OUTPUT
        self.auto_write = auto_write

    def __setitem__(self, index: Union[int, slice], val: Union[tuple[int, int, int], Sequence[tuple[int, int, int]]]):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._nums)
            for val_index, i in enumerate(range(start, stop, step)):
                self._set_item(i, val[val_index])
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
        if isinstance(val, int):
            val = (val >> 16, val >> 8, val)
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
        if self.brightness < 1.0:
            # apply brightness
            buf = bytearray(len(self.buf))
            for i, val in enumerate(self.buf):
                buf[i] = int(val * self.brightness)
            self._transmit(buf)
        else:
            self._transmit(self.buf)

    def _transmit(self, buf):
        neopixel_write(self.pin, buf)
