from time import sleep, perf_counter_ns

import arrow
from loguru import logger

import numpy

from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.physical.driver import lcd
from rpi_ws281x import PixelStrip, Color
from gpiozero import Button
from subprocess import check_call
from multiprocessing import Process, Queue
import queue

def lcd_update_process(display: lcd, message_queue: Queue):
    display.lcd_clear()
    while True:
        message = message_queue.get()
        display.lcd_display_string(message[:16], 1)
        display.lcd_display_string(message[16:], 2)

class MatrixScreen(ScreenBase):

    __next_flag = False

    def __init__(self):
        logger.info("Initializing Matrix Screen (Physical)")
        self.__brightness = 0.05
        self.__pixels = PixelStrip(1024, 18, 800000, 10, False, 255, 0)
        # 1024 pixels on pin 18, 800000 hz frequency on DMA channel 10, noninverting, brightness adjusted, on channel 0
        self.__pixels.begin()

        # Button(pin, pull_up, active_state, bounce_time, hold_time, hold_repeat, pin_factory)
        self.__next_button = Button(12, pull_up=None, active_state=True, bounce_time=0.050, hold_time=15)
        MatrixScreen.__next_flag = False # A flag that the button will set to true and be unset whenever it is handled.
        self.__next_button.when_pressed = MatrixScreen.__handle_next_button_press
        self.__next_button.when_held = MatrixScreen.__handle_shutdown_press

        self.__lcd = lcd()
        self.__lcd_text_queue = Queue()
        self.__lcd_process = Process(target=lcd_update_process, args=(self.__lcd, self.__lcd_text_queue,))
        self.__lcd_process.start()
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

        self._last_update = perf_counter_ns()

        # Finished table generation, now load screen...
        self.loading_screen()

    def update_display(self, canvas: Canvas):
        # Apply gamma correction
        gamma = 2.8 # Who knows if this'll look nice at all
        m_in = 255
        m_out = int(self.__brightness * 255)

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

        now = perf_counter_ns()
        delay = (1/24)*1000000000 - (now - self._last_update)
        end = now + delay
        sleep(max(0, (delay/1000000000)-0.001))
        while now < end:
            now = perf_counter_ns()
        self._last_update = perf_counter_ns()

    def update_lcd(self, text):
        if text == self.__cached_text:
            return
        logger.debug("Updating LCD with text: {}", text)
        if len(text) != 32:
            logger.error("Text is not 32 characters! {}", text)
        # self.__lcd.lcd_clear()
        try:
            self.__lcd_text_queue.put(text, block=False)
        except queue.Full:
            logger.error("Attempted to enqueue LCD text, but the queue was full!")
        self.__cached_text = text

    def __handle_next_button_press():
        MatrixScreen.__next_flag = True
        logger.debug("Next button pressed.")

    def __handle_shutdown_press():
        logger.info("Shutdown button pressed! Shutting down...")
        check_call(["sudo", "poweroff"])

    def force_next_task(self, screen_manager):
        if MatrixScreen.__next_flag:
            MatrixScreen.__next_flag = False
            logger.debug("Received request to skip to next task.")
            screen_manager.next_task()
