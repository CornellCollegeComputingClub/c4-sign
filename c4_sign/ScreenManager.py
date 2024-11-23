import importlib
from datetime import timedelta
import random
import subprocess
import os
import sys
from typing import Union
from pathlib import Path
from time import sleep

from loguru import logger

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JError

from c4_sign.base_task import OptimScreenTask, ScreenTask, JavaTask
from c4_sign.lib.canvas import Canvas
from c4_sign.loading_manager import LoadingManager


class ScreenManager:
    def __init__(self, make_histograms, enable_java):
        self.tasks = []
        self.current_task = None
        self.index = 0
        self.make_histograms = make_histograms
        self.java_enabled = enable_java

    @property
    def current_tasks(self) -> list[ScreenTask]:
        return self.tasks

    def update_tasks(self, loading_manager: Union[None, LoadingManager] = None):
        # import all files in screen_tasks
        logger.info("Updating screen tasks")
        mod = importlib.import_module("c4_sign.screen_tasks")
        for obj in mod.__all__:
            obj = importlib.import_module(f"c4_sign.screen_tasks.{obj}")
            for name, obj in obj.__dict__.items():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, ScreenTask)
                    and obj not in (ScreenTask, OptimScreenTask, JavaTask)
                    and obj.ignore is False
                ):
                    logger.debug("Adding screen task: {}", obj.__name__)
                    if loading_manager:
                        with loading_manager(obj.__name__):
                            instance = obj()
                            instance.set_make_histogram(self.make_histograms)
                            self.tasks.append(instance)
                    else:
                        instance = obj()
                        instance.set_make_histogram(self.make_histograms)
                        self.tasks.append(instance)
                    logger.debug("Screen Task {} added!", obj.__name__)


        if self.java_enabled:
            # start java server!

            java_server_script_path = Path(os.path.abspath(os.path.dirname(__file__))) / ".." / "tools" / "start_java_server.py"

            subprocess.Popen(["python", java_server_script_path])

            # Next load the java tasks!
            gateway = JavaGateway()
            java_task_controller = None
            tasks = None
            attempts = 0

            while tasks is None and attempts < 30:
                try:
                    java_task_controller = gateway.entry_point
                    tasks = java_task_controller.getActiveTasks()
                except Py4JError:
                    java_task_controller = None
                    tasks = None
                finally:
                    sleep(0.25)
                    logger.info("Waiting for java server to start...")
                attempts += 1

            if java_task_controller is None or tasks is None:
                logger.error("Unable to establish connection to Py4J Gateway Server!")
                logger.error("Did you remember to compile the java project with tools/compile_java_project.py?")
                logger.error("If you don't want to run Java tasks, run the command again with the --disable-java flag.")
                sys.exit(1)

            tasks = java_task_controller.getActiveTasks()

            logger.info("Connection to Py4J Gateway Server established!")

            logger.debug("Java tasks discovered!")
            for task in tasks:
                if loading_manager:
                    with loading_manager(task.getTitle()):
                        instance = JavaTask(task)
                        instance.set_make_histogram(self.make_histograms)
                        self.tasks.append(instance)
                else:
                    instance = JavaTask(task)
                    instance.set_make_histogram(self.make_histograms)
                    self.tasks.append(instance)
                logger.debug("Screen Task {} added!", task.getTitle())
        else:
            logger.warning("Java tasks are disabled! This is fine on the simulator, but make sure they're enabled in the physical display!")

        # now, shuffle the tasks with an arbitrary seed (so that it's the same between simulator and real)
        rand = random.Random(0xd883ff)
        rand.shuffle(self.tasks)
        logger.info("Screen Tasks updated!")

    def override_current_task(self, task: Union[str, ScreenTask]):
        # if task is a string, find the task by name
        if isinstance(task, str):
            for t in self.tasks:
                if t.title == task:
                    task = t
                    break
            else:
                # task not found!
                logger.warning(f"Task {task} not found!")
                return
        logger.info("Overriding current task with {}", task.title)
        if self.current_task:
            self.current_task.teardown(True)
        self.current_task = task
        self.current_task.prepare()
        self.index = -1

    def draw(self, canvas: Canvas, delta_time: timedelta):
        if not self.current_task:
            logger.debug("No current task!")
            if self.index >= len(self.current_tasks):
                logger.debug("Looping back to the start!")
                self.index = 0
            self.current_task = self.current_tasks[self.index]
            logger.debug("Trying to start task: {}", self.current_task.__class__.__name__)
            if not self.current_task.prepare():
                # uh... we don't want to do anything!
                # so let's just skip this task!
                logger.debug("Task {} not ready, skipping!", self.current_task)
                self.current_task = None
                self.index += 1
                if self.index >= len(self.current_tasks):
                    self.index = 0
                return self.draw(canvas, delta_time)
            logger.debug("Task {} ready!", self.current_task.__class__.__name__)
        if self.current_task.draw(canvas, delta_time):
            logger.debug("Task {} finished!", self.current_task.__class__.__name__)
            self.current_task = None
            self.index += 1
            return True
        return False

    def get_lcd_text(self):
        if self.current_task:
            return self.current_task.get_lcd_text()
        else:
            return " " * 32
