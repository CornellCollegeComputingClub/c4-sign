from threading import Thread
from time import sleep

from loguru import logger

from c4_sign.lib.screen.base import ScreenBase
from c4_sign.lib.screen.simulator import SimulatorScreen


class LoadingManager:
    def __call__(self, text):
        """
        Called before __enter__.
        """
        return self

    def __enter__(self):
        """
        Start
        """
        return self
    
    def __exit__(self, *args):
        """
        End
        """
        pass

class DebugLoadingManager(LoadingManager):
    def __call__(self, text):
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

class ScreenLoadingManager(LoadingManager):
    def __init__(self, screen: ScreenBase):
        self.screen = screen
        self.is_simulator = isinstance(screen, SimulatorScreen)
        self.text = ""
        self.delay_thread = None
        self.delay_thread_should_stop = False

    def __call__(self, text):
        self.text = text
        self.delay_thread_should_stop = False
        return self

    def __enter__(self):
        # after a second, update the screen with text
        self.delay_thread = Thread(target=self.delayed_update)
        self.delay_thread_should_stop = False
        self.delay_thread.start()
        return self

    def delayed_update(self):
        if not self.is_simulator:
            sleep(1)
        if self.delay_thread_should_stop:
            return
        self.screen.loading_cb(self.text)

    def __exit__(self, *args):
        if self.delay_thread.is_alive():
            self.delay_thread_should_stop = True
            self.delay_thread.join()
        self.text = ""
        self.screen.loading_cb(self.text)
