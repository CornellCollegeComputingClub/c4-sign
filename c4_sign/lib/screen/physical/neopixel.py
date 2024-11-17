from typing import Sequence, Union

from loguru import logger

from rpi_ws281x import PixelStrip, Color
from threading import Lock
from copy import deepcopy


class NeoPixel:
    def __init__(self, pin, num_pixels, brightness=1.0, auto_write=True):
        logger.debug("Initializing NeoPixels")
        self.buf = bytearray(3 * num_pixels)
        self._nums = num_pixels
        self.brightness = brightness
        # brightness is 255 here because we apply it ourselves
        # no need for double dimming
        self.strip = PixelStrip(num_pixels, pin, 800000, 10, False, 255, 0)
        self.strip.begin()
        self.auto_write = auto_write
        self._lock = Lock()

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
        # neopixels use GRB, but rpi_ws281x uses RGB.
        if index < 0:
            index += len(self)
        if index >= self._nums or index < 0:
            raise IndexError
        offset = index * 3
        if isinstance(val, int):
            val = (val >> 16, val >> 8, val)
        self.buf[offset] = val[0]  # red
        self.buf[offset + 1] = val[1]  # green
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
            logger.trace("Applying brightness")
            # apply brightness
            buf = bytearray(len(self.buf))
            for i, val in enumerate(self.buf):
                buf[i] = int(val * self.brightness)
            self._transmit(buf)
        else:
            self._transmit(deepcopy(self.buf))

    def _transmit(self, buf):
        with self._lock:
            logger.trace("Transmitting to NeoPixels")
            for i in range(len(buf) // 3):
                self.strip[i] = Color(buf[i * 3], buf[i * 3 + 1], buf[i * 3 + 2])
            self.strip.show()
            logger.trace("Transmission complete!")
