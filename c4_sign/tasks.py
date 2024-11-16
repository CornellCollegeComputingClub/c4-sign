from datetime import timedelta

import arrow
from loguru import logger

from c4_sign.base_task import RepeatingTask
from c4_sign.consts import DEV_MODE
from c4_sign.update import check_for_updates


class UpdateTask(RepeatingTask):
    def __init__(self):
        if DEV_MODE:
            super().__init__(timedelta(minutes=15))
        else:
            super().__init__(timedelta(days=1))
            self.last_run = arrow.now().replace(hour=0, minute=5, second=0, microsecond=0)  # run just after midnight

    def on_run(self):
        if check_for_updates():
            exit(5)


class TaskManager:
    def __init__(self):
        self.tasks = []

    def setup_tasks(self):
        logger.info("Setting up tasks")
        self.add_task(UpdateTask())

    def add_task(self, task):
        logger.debug("Adding task: {}", task.__class__.__name__)
        self.tasks.append(task)

    def check_and_run_tasks(self):
        for task in self.tasks:
            task.check_and_run()

    def run_tasks(self):
        logger.debug("Running all tasks manually")
        for task in self.tasks:
            task.run()
