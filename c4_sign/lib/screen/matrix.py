import threading

from loguru import logger

import board
import numpy

from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.physical.driver import lcd
from c4_sign.lib.screen.physical.neopixel import NeoPixel


class MatrixScreen(ScreenBase):
    def __init__(self):
        logger.info("Initializing Matrix Screen (Physical)")
        self.__pixels = NeoPixel(board.D18, 32 * 32, brightness=0.05, auto_write=False)
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

        # Finished table generation, now load screen...
        self.loading_screen()

    def update_display(self, canvas: Canvas):
        logger.trace("Updating display...")
        # for i in range(32*32):
        #     self.__pixels[i] = canvas[i]
        self.__pixels[:] = canvas.data.reshape((1024, 3))[self.__address_table]
        if self.__draw_thread is not None:
            logger.trace("Joining old draw thread...")
            self.__draw_thread.join()
        logger.trace("Starting new draw thread...")
        self.__draw_thread = threading.Thread(target=self.__pixels.show)
        self.__draw_thread.start()
        # self.__pixels[:] = canvas.data.reshape((1024, 3))[self.__address_table]
        # self.__pixels.show()

    def update_display_thread(self, canvas):
        # self.__pixels[:] = canvas.data.reshape((1024, 3))[self.__address_table]
        self.__pixels.show()

    def update_lcd(self, text):
        if text == self.__cached_text:
            return
        logger.debug("Updating LCD with text: {}", text)
        self.__lcd.lcd_clear()
        self.__lcd.lcd_display_string(text[:16], 1)
        self.__lcd.lcd_display_string(text[16:], 2)
        self.__cached_text = text
