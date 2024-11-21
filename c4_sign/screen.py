import arrow
from loguru import logger

from c4_sign.consts import DEV_MODE
from c4_sign.lib.canvas import Canvas
from c4_sign.loading_manager import LoadingManager
from c4_sign.screen_tasks.error import ErrorScreenTask
from c4_sign.ScreenManager import ScreenManager


class Screen:
    __screen = None
    __screen_manager = None
    __last_update = arrow.now()
    __canvas = Canvas()
    __low_fps_counter = 0

    def init_matrix(self, simulator: bool, histograms = False):
        if simulator:
            from c4_sign.lib.screen.simulator import SimulatorScreen

            self.__screen = SimulatorScreen()
        else:
            from c4_sign.lib.screen.matrix import MatrixScreen

            self.__screen = MatrixScreen()
        self.__screen_manager = ScreenManager(histograms)

        lm = LoadingManager(self.__screen)
        self.__screen_manager.update_tasks(lm)

    def screen_active(self):
        if DEV_MODE:
            return True
        now = arrow.now()
        # normal hours! between 6 am and midnight.
        return now.hour >= 6 and now.hour < 24

    def update_screen(self):
        now = arrow.now()
        delta_t = now - self.__last_update
        self.__last_update = now

        text = self.__screen_manager.get_lcd_text()
        self.__screen.update_lcd(text)

        # clear canvas
        canvas = self.__canvas
        canvas.clear()

        # brightness
        if self.screen_active():
            self.__screen.brightness = 100
        else:
            self.__screen.brightness = 0
            self.__screen.update_display(canvas)
            return  # don't draw anything!

        # draw stuff
        try:
            self.__screen_manager.draw(canvas, delta_t)
        except Exception as e:
            logger.error("Caught exception while drawing screen!")
            logger.exception(e)
            self.__screen_manager.override_current_task(ErrorScreenTask(e))

        self.__screen.update_display(canvas)
        fps = 1 / delta_t.total_seconds()
        if fps < 20:
            self.__low_fps_counter += 1
            if self.__low_fps_counter > 6:  # .25 seconds
                logger.warning("Low FPS! {}", fps)
                self.__low_fps_counter = 0  # reset counter so we don't spam the logs
        else:
            self.__low_fps_counter = 0
        self.__screen.debug_info(
            fps=fps,
            brightness=self.__screen.brightness,
            current_task=self.__screen_manager.current_task.__class__.__name__,
            tasks=[t.__class__.__name__ for t in self.__screen_manager.tasks],
            task_time_elapsed=(
                self.__screen_manager.current_task.elapsed_time.total_seconds()
                if self.__screen_manager.current_task
                else None
            ),
            task_suggested_run_time=(
                self.__screen_manager.current_task.suggested_run_time.total_seconds()
                if self.__screen_manager.current_task
                else None
            ),
            task_max_run_time=(
                self.__screen_manager.current_task.max_run_time.total_seconds()
                if self.__screen_manager.current_task
                else None
            ),
        )
        self.__screen.debug_override(self.__screen_manager)
    
    @property
    def screen(self):
        return self.__screen
    
    @property
    def screen_manager(self):
        return self.__screen_manager
