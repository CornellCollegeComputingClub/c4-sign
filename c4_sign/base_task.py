import arrow
from datetime import timedelta

from c4_sign.consts import COLOR_GRAY, COLOR_PURPLE, FONT_4x6

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
    def __init__(self, suggested_run_time=timedelta(), max_run_time=timedelta()):
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

    def draw_header(self, canvas):
        now = arrow.now()
        current_time = now.format("h:mm").rjust(5)
        current_date = now.format("ddd,MMM D")
        graphics.DrawLine(canvas, 0, 7, 63, 7, COLOR_GRAY)
        graphics.DrawLine(canvas, 21, 0, 21, 7, COLOR_GRAY)
        graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_PURPLE, current_time)
        graphics.DrawText(canvas, FONT_4x6, 23, 6, COLOR_PURPLE, current_date)
    
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
    
    def draw(self, canvas, delta_time):
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
    def draw_frame(self, canvas, delta_time):
        # override this method to run code when the screen is updated!
        # return True if you're done updating!
        raise NotImplementedError
    
    @classmethod
    def construct_from_config(cls, config):
        # override this method to construct a task from a config!
        raise NotImplementedError

