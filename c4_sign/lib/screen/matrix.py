from time import sleep

import arrow
from loguru import logger

import numpy

from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.physical.driver import lcd
from rpi_ws281x import PixelStrip, Color


class MatrixScreen(ScreenBase):
    def __init__(self):
        logger.info("Initializing Matrix Screen (Physical)")
        brightness = 0.05
        self.__pixels = PixelStrip(1024, 18, 800000, 10, False, int(brightness * 255), 0)
        # 1024 pixels on pin 18, 800000 hz frequency on DMA channel 10, noninverting, brightness adjusted, on channel 0
        self.__pixels.begin()

        self.__lcd = lcd()
        self.__cached_text = " " * 32

        # Generating address table...
        logger.debug("Generating address table...")
        quadrant_one = []

        # Generate the zigzag for one quadrant.
        for i in range(0, 8):
            row1, row2 = [], []
            for j in range(15, -1, -1):
                row1.append(i * 32 + j)

            for j in range(0, 16):
                row2.append((i * 32) + 16 + j)

            quadrant_one.append(row1)
            quadrant_one.append(row2)

        # Add constant offset to all four quadrants.
        from copy import deepcopy

        top_right = quadrant_one
        top_left = [[y + 256 for y in x] for x in deepcopy(quadrant_one)]
        bot_right = [[y + 512 for y in x] for x in deepcopy(quadrant_one)]
        bot_left = [[y + 768 for y in x] for x in deepcopy(quadrant_one)]

        for i, x in enumerate(top_left):
            x.extend(top_right[i])

        for i, x in enumerate(bot_left):
            x.extend(bot_right[i])

        top_left.extend(bot_left)

        self.__address_table = numpy.argsort(numpy.array(top_left).reshape(1024))
        # 1024-long list of addresses
        logger.debug("Address table generated.")

        self.__draw_thread = None

        self._last_update = arrow.now()

        # Finished table generation, now load screen...
        self.loading_screen()

    def update_display(self, canvas: Canvas):
        # Apply gamma correction
        gamma = 2.8 # Who knows if this'll look nice at all
        m_in = 255
        m_out = 255

        a = canvas.data.astype(numpy.float32)
        a /= m_in
        a **= gamma
        a *= m_out
        a += 0.5
        a = a.astype(numpy.uint8)

        f = lambda c: Color(int(c[0]), int(c[1]), int(c[2]))
        colors = list(map(f, a.reshape((1024, 3))[self.__address_table]))
        for i in range(1024):
            self.__pixels[i] = colors[i]
        self.__pixels.show()
        now = arrow.now()
        sleep(max(0, (1 / 24) - (now - self._last_update).total_seconds()))
        self._last_update = arrow.now()

    def update_lcd(self, text):
        if text == self.__cached_text:
            return
        logger.debug("Updating LCD with text: {}", text)
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string(text[:16], 1)
        self.__lcd.lcd_display_string(text[16:], 2)
        self.__cached_text = text
