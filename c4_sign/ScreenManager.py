import importlib

from c4_sign.base_task import ScreenTask

class ScreenManager:
    def __init__(self):
        self.tasks = []
        self.current_task = None
        self.index = 0

    @property
    def current_tasks(self):
        return self.tasks

    def update_tasks(self):
        # import all files in screen_tasks
        mod = importlib.import_module("c4_sign.screen_tasks")
        for obj in mod.__all__:
            obj = importlib.import_module(f"c4_sign.screen_tasks.{obj}")
            for name, obj in obj.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, ScreenTask) and obj != ScreenTask and obj.ignore is False:
                    self.tasks.append(obj())

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
    
    def get_lcd_text(self):
        if self.current_task:
            return self.current_task.get_lcd_text()
        else:
            return " " * 32
        
        