import multiprocessing
from time import sleep

from c4_sign.emulator.__main__ import start_server
from c4_sign.lib.canvas import Canvas
from c4_sign.lib.screen.base import ScreenBase


class SimulatorScreen(ScreenBase):
    def __init__(self):
        super().__init__()
        self._to_web = multiprocessing.Queue()
        self._from_web = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=start_server, args=(self._to_web, self._from_web))
        self._process.start()

    def update_lcd(self, text):
        self._to_web.put({"type": "lcd", "text": text})

    def update_display(self, canvas: Canvas):
        self._to_web.put({"type": "display", "canvas": canvas.serialize()})
        sleep(1 / 24)  # 24 fps
