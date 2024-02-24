from datetime import timedelta

import arrow

from c4_sign.consts import COLOR_GRAY, COLOR_PURPLE, FONT_4x6
from c4_sign.lib.canvas import Canvas


class RepeatingTask:
    def __init__(self, interval, func=None):
        self.interval = interval
        self.func = func
        self.last_run = arrow.now()

    @property
    def since_last_run(self):
        return arrow.now() - self.last_run

    @property
    def time_until_next_run(self):
        return self.interval - self.since_last_run

    def check(self):
        if self.since_last_run >= self.interval:
            return True
        return False

    def check_and_run(self):
        if self.check():
            self.run()

    def run(self):
        if self.func:
            self.func()
        else:
            self.on_run()
        self.last_run = arrow.now()

    def on_run(self):
        # override this method to run code when the task is run!
        pass


class OneTimeTask:
    def __init__(self, run_at, func=None):
        self.run_at = run_at
        self.func = func

    def check(self):
        if arrow.now() >= self.run_at:
            return True
        return False

    def check_and_run(self):
        if self.check():
            self.run()

    def run(self):
        if self.func:
            self.func()
        else:
            self.on_run()

    def on_run(self):
        # override this method to run code when the task is run!
        pass


class ScreenTask:
    ignore = False
    title = "Unknown"
    artist = "Unknown"

    def __init__(
        self,
        suggested_run_time=timedelta(seconds=30),
        max_run_time=timedelta(seconds=60),
    ):
        self.started = None
        self.elapsed_time = timedelta()
        self.suggested_run_time = suggested_run_time
        if max_run_time < suggested_run_time:
            max_run_time = suggested_run_time
        self.max_run_time = max_run_time

    def set_suggested_run_time(self, suggested_run_time):
        self.suggested_run_time = suggested_run_time
        if self.max_run_time < suggested_run_time:
            self.max_run_time = suggested_run_time

    def set_max_run_time(self, max_run_time):
        self.max_run_time = max_run_time

    def prepare(self):
        """
        This method is called when the task is first run.

        If this method returns False, the task will be skipped.

        If this method returns True, the task will be run.
        """
        # do any setup here!
        self.started = arrow.now()
        self.elapsed_time = timedelta()

        # return True if we WANT to do anything!
        # this is useful for, say, critical weather updates
        # if there's nothing needed, why do we need to run?
        return True

    """
    This method is called when the task is done running.
    """

    def teardown(self, forced=False):
        # do any cleanup here!
        pass

    def draw(self, canvas: Canvas, delta_time: timedelta):
        # override draw_frame!
        # returns True if we're done updating!
        self.elapsed_time += delta_time
        result = self.draw_frame(canvas, delta_time)
        if self.is_over_max_time:
            self.teardown(forced=True)
            return True
        if result and self.is_over_suggested_time:
            self.teardown()
            return True
        return False

    @property
    def is_over_max_time(self):
        return self.elapsed_time > self.max_run_time

    @property
    def is_over_suggested_time(self):
        return self.elapsed_time > self.suggested_run_time

    """
    This method is called for every frame of the task.

    If this method returns False, the task will continue to run.

    If this method returns True, the task will be stopped soon after!
    """

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:
        # override this method to run code when the screen is updated!
        # return True if you're done updating!
        raise NotImplementedError

    """
    This method is called every time the LCD screen is updated.
    
    Returns a 32 character string to display on the LCD screen.
    """

    def get_lcd_text(self) -> str:
        # override this method to return text for the LCD screen!
        # by default, we're gonna return something like:
        # "Title"
        # "By: Artist"
        # but since this is a 16x2 screen, we have to truncate (if needed)
        # and pad with spaces!
        title = self.title.center(16)
        artist = "By: " + self.artist
        artist = artist.center(16)
        return title + artist
