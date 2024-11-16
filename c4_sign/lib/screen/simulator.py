import multiprocessing
from time import sleep

import arrow
from loguru import logger

from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase


class SimulatorScreen(ScreenBase):
    def __init__(self):
        from c4_sign.emulator.__main__ import start_server
        self._to_web = multiprocessing.Queue()
        self._from_web = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=start_server, args=(self._to_web, self._from_web))
        logger.info("Starting simulator server")
        self._process.start()
        self._last_update = arrow.now()
        super().loading_screen()

    def update_lcd(self, text):
        logger.trace("Updating LCD with {}", text)
        self._to_web.put({"type": "lcd", "text": text})

    def update_display(self, canvas: Canvas):
        logger.trace("Updating display")
        self._to_web.put({"type": "display", "canvas": canvas.serialize()})
        now = arrow.now()
        # sleep so we fill a 1/24th of a second
        logger.trace("Finished updating display, sleeping")
        sleep(max(0, (1 / 24) - (now - self._last_update).total_seconds()))
        self._last_update = arrow.now()

    def debug_info(self, **kwargs):
        logger.trace("Sending debug info: {}", kwargs)
        self._to_web.put({"type": "debug_info", "data": kwargs})

    def debug_override(self, screen_manager):
        if self._from_web.empty():
            return
        data = self._from_web.get()
        if data["type"] == "override":
            logger.debug("Recieved request to override current task with {}", data["task"])
            screen_manager.override_current_task(data["task"])
