import importlib
from datetime import timedelta
from typing import Union

from c4_sign.base_task import ScreenTask
from c4_sign.lib.canvas import Canvas


class ScreenManager:
    def __init__(self):
        self.tasks = []
        self.current_task = None
        self.index = 0

    @property
    def current_tasks(self) -> list[ScreenTask]:
        return self.tasks

    def update_tasks(self):
        # import all files in screen_tasks
        mod = importlib.import_module("c4_sign.screen_tasks")
        for obj in mod.__all__:
            obj = importlib.import_module(f"c4_sign.screen_tasks.{obj}")
            for name, obj in obj.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, ScreenTask) and obj != ScreenTask and obj.ignore is False:
                    self.tasks.append(obj())

    def override_current_task(self, task: Union[str, ScreenTask]):
        # if task is a string, find the task by name
        if isinstance(task, str):
            for t in self.tasks:
                if t.__class__.__name__ == task:
                    task = t
                    break
            else:
                # task not found!
                print(f"Task {task} not found!")
                return
        if self.current_task:
            self.current_task.teardown(True)
        self.current_task = task
        self.current_task.prepare()
        self.index = -1

    def draw(self, canvas: Canvas, delta_time: timedelta):
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
