import requests
from c4_sign.screen_tasks.now_playing import KRNLNowPlaying
from c4_sign.screen_tasks.psa import RandomPSA


class ScreenManager:
    def __init__(self):
        self.live_tasks = []
        self.not_live_tasks = []
        self.current_task = None
        self.index = 0

    @property
    def current_tasks(self):
        return self.tasks

    def update_tasks(self):
        # TODO: replace this with locally stored data
        live_req = requests.get("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/live_layout.json")
        self.tasks = []
        pass

    def override_current_task(self, task):
        if self.current_task:
            self.current_task.teardown(True)
        self.current_task = task
        self.current_task.prepare()
        self.index = -1

    def draw(self, canvas, delta_time):
        if not self.current_task:
            if self.index >= len(self.current_tasks):
                self.index = 0
            self.current_task = self.current_tasks[self.index]
            if not self.current_task.prepare():
                # uh... we don't want to do anything!
                # so let's just skip this task!
                self.current_task = None
                self.index += 1
                if self.index >= len(self.current_tasks):
                    self.index = 0
                return self.draw(canvas, delta_time)
        if self.current_task.draw(canvas, delta_time):
            self.current_task.teardown()
            self.current_task = None
            self.index += 1
            return True
        return False
        