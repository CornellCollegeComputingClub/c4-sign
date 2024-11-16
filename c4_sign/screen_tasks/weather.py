from datetime import timedelta

import arrow
from loguru import logger

from c4_sign.base_task import ScreenTask
from c4_sign.consts import COLOR_GRAY, COLOR_RED, COLOR_WHITE, FONT_PICO
from c4_sign.lib import graphics
from c4_sign.util import internet_is_available, lerp, map_value, requests_get_1hr_cache

WEATHER_CODES = {
    # have to be 8 chars or less
    0: "Clear",
    1: "MosClear",
    2: "PtlyCldy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "LtDriz",
    53: "Drizzle",
    55: "HvyDriz",
    56: "FrzDriz",
    57: "FrzDriz",
    61: "LtRain",
    63: "Rain",
    65: "HvyRain",
    66: "FrzRain",
    67: "FrzRain",
    71: "LtSnow",
    73: "Snow",
    75: "HvySnow",
    77: "Sleet",
    80: "LtShwr",
    81: "Showers",
    82: "HvyShwr",
    85: "SnowShwr",
    86: "SnowShwr",
    95: "TStorm",
    96: "TStorm",
    99: "TStorm",
}


class Weather(ScreenTask):
    title = "Weather"
    artist = "Luna"

    def __init__(self):
        for k, v in WEATHER_CODES.items():
            if len(v) > 8:
                logger.error(f"WEATHER_CODES[{k}] = {v} is too long! Must be 8 chars or less.")
        super().__init__()

    def prepare(self):
        if not internet_is_available():
            return False
        data = requests_get_1hr_cache(
            "https://api.open-meteo.com/v1/forecast?latitude=41.922&longitude=-91.4168&hourly=temperature_2m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timeformat=unixtime&timezone=America%2FChicago"
        )
        self.report = data.json()
        self.now = arrow.now()
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        if self.elapsed_time < timedelta(seconds=10):
            return self.draw_current_weather(canvas)
        elif self.elapsed_time < timedelta(seconds=20):
            return self.draw_forecast_today(canvas, 0)
        elif self.elapsed_time < timedelta(seconds=30):
            return self.draw_forecast_today(canvas, 1)
        elif self.elapsed_time < timedelta(seconds=40):
            return self.draw_forecast_today(canvas, 2)
        else:
            self.draw_forecast_daily_future(canvas, (self.elapsed_time.total_seconds() - 40) // 10)

    def draw_current_weather(self, canvas):
        graphics.draw_centered_text(canvas, FONT_PICO, 6, COLOR_GRAY, "Current")
        # find current temperature.
        # if we're between two hours, interpolate the temperature.
        for i, time in enumerate(self.report["hourly"]["time"]):
            # tz = America/Chicago
            if arrow.get(time) > self.now:
                break
        else:
            i = -1
        if i == 0:
            temp = self.report["hourly"]["temperature_2m"][0]
        else:
            temp = lerp(
                self.report["hourly"]["temperature_2m"][i - 1],
                self.report["hourly"]["temperature_2m"][i],
                (self.now.timestamp() - self.report["hourly"]["time"][i - 1])
                / (self.report["hourly"]["time"][i] - self.report["hourly"]["time"][i - 1]),
            )

        # find max and min temperature for the day
        max_temp = self.report["daily"]["temperature_2m_max"][i // 24]
        min_temp = self.report["daily"]["temperature_2m_min"][i // 24]

        graphics.draw_centered_text(canvas, FONT_PICO, 31, COLOR_WHITE, str(round(temp, 1)) + "F")
        graphics.stroke_line(canvas, 0, 31, round(map_value(temp, min_temp, max_temp, 1, 32)), 31, COLOR_RED)
        graphics.draw_centered_text(
            canvas,
            FONT_PICO,
            13,
            COLOR_WHITE,
            WEATHER_CODES.get(self.report["hourly"]["weather_code"][i // 24], "Unknown"),
        )

    def draw_forecast_today(self, canvas, i):
        # i = (8:30 - 9), 11a, 3p
        # i = 0, 1, 2
        # so! let's do this!
        # 0: 8:30 - 9 (use 8:45 am)
        # 1: 11a
        # 2: 3p

        # find and draw the time (for that hour)
        target_times = ["8:45", "11:00", "15:00"]
        # self.now is arrow obj
        # merge with the date of self.now
        target_times = [
            self.now.floor("day").replace(hour=int(t.split(":")[0]), minute=int(t.split(":")[1])) for t in target_times
        ]
        # target_times = [now.floor("day").replace(hour=int(t.split(":")[0]), minute=int(t.split(":")[1])) for t in target_times]
        for j, time in enumerate(self.report["hourly"]["time"]):
            if arrow.get(time) > target_times[i]:
                break
        else:
            raise ValueError("No time found!")
        if j == 0:
            temp = self.report["hourly"]["temperature_2m"][0]
        else:
            temp = lerp(
                self.report["hourly"]["temperature_2m"][j - 1],
                self.report["hourly"]["temperature_2m"][j],
                (target_times[i].timestamp() - self.report["hourly"]["time"][j - 1])
                / (self.report["hourly"]["time"][j] - self.report["hourly"]["time"][j - 1]),
            )
        max_temp = self.report["daily"]["temperature_2m_max"][j // 24]
        min_temp = self.report["daily"]["temperature_2m_min"][j // 24]
        graphics.draw_centered_text(canvas, FONT_PICO, 6, COLOR_GRAY, target_times[i].format("h:mm A"))
        graphics.draw_centered_text(canvas, FONT_PICO, 31, COLOR_WHITE, str(round(temp, 1)) + "F")
        graphics.stroke_line(canvas, 0, 31, round(map_value(temp, min_temp, max_temp, 1, 32)), 31, COLOR_RED)
        graphics.draw_centered_text(
            canvas, FONT_PICO, 13, COLOR_WHITE, WEATHER_CODES.get(self.report["hourly"]["weather_code"][j], "Unknown")
        )

    def draw_forecast_daily_future(self, canvas, i):
        # i = days to look ahead
        # find and draw the time (for that day)
        target = self.now.floor("day").shift(days=i)
        for j, time in enumerate(self.report["daily"]["time"]):
            if arrow.get(time) > target:
                break
        else:
            raise ValueError("No time found!")
        max_temp = self.report["daily"]["temperature_2m_max"][j]
        min_temp = self.report["daily"]["temperature_2m_min"][j]
        graphics.draw_centered_text(canvas, FONT_PICO, 6, COLOR_GRAY, target.format("dddd"))
        graphics.draw_centered_text(canvas, FONT_PICO, 20, COLOR_WHITE, str(round(max_temp, 1)) + "F")
        graphics.draw_centered_text(canvas, FONT_PICO, 31, COLOR_WHITE, str(round(min_temp, 1)) + "F")

        # draw the weather code
        graphics.draw_centered_text(
            canvas, FONT_PICO, 13, COLOR_WHITE, WEATHER_CODES.get(self.report["daily"]["weather_code"][j], "Unknown")
        )
