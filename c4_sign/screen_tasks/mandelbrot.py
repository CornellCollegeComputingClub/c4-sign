import math
import random
from dataclasses import dataclass
from datetime import timedelta

from c4_sign.base_task import OptimScreenTask
from c4_sign.lib.canvas import Canvas


class Mandelbrot(OptimScreenTask):
    title = "Mandelbrot Set"
    artist = "Mac Coleman"

    def prepare(self):
        self.center = complex(0, 0)
        self.scale = 4
        self.frame = 0
        self.iterations = 1
        self.max_iterations = 150
        self.intro_time = 140
        self.epic_points = [
            complex(-1.7692505972726005, 0.05691909790039061),
            complex(-1.9426247732979907, 0),
            complex(-0.10539082118443051, -0.9248651776994978),
            complex(-0.7464179992675776, 0.18429674421037967),
            complex(-1.0200429643903455, 0.36748341151646224),
            complex(0.42451275246484, 0.2075301834515165),
            complex(-1.2840499877929685, 0.427382332938058),
            complex(0.3577270507812499, -0.11002349853515625),
            complex(-1.985455104282924, 0),
            complex(-1.2517939976283483, 0.0411834716796875),
        ]
        sign = random.choice([1, -1])
        self.chosen_point = random.choice(self.epic_points)
        self.chosen_point = complex(self.chosen_point.real, self.chosen_point.imag * sign)
        return super().prepare()

    def get_lcd_text(self) -> str:
        mrt = self.max_run_time.total_seconds()
        et = self.elapsed_time.total_seconds()
        if self.frame < self.intro_time or mrt - et < 5.0:
            return super().get_lcd_text()

        if 20 < et < 40:
            return "in the land of".center(16) + "the imaginary!".center(16)
        elif 40 <= et:
            return f"a = {self.chosen_point.real:12.8f}".center(16) + f" + {self.chosen_point.imag:12.8f}i".center(16)
        else:
            return "Come with me on".center(16) + "a journey...".center(16)

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:

        x_min = 0
        x_max = 31
        y_min = 0
        y_max = 31

        u_min = self.center.real - self.scale / 2
        u_max = self.center.real + self.scale / 2
        v_min = self.center.imag - self.scale / 2
        v_max = self.center.imag + self.scale / 2

        for x in range(0, 32):
            for y in range(0, 32):
                u = u_min + (u_max - u_min) * (x - x_min) / (x_max - x_min)
                v = v_min + (v_max - v_min) * (y - y_min) / (y_max - y_min)

                z = complex(0, 0)
                c = complex(u, v)

                # 2-bulb check
                if abs(c + 1) ** 2 <= 0.0625:
                    continue  # Don't do anything if inside two-bulb

                # Cardioid check
                q = (u - 1 / 4) * (u - 1 / 4) + v * v

                if q * (q + (u - 1 / 4)) <= 1 / 4 * v**2:
                    continue  # Don't do any tests if inside cardioid

                count = 0
                while abs(z) ** 2 < 4.0 and count < self.iterations:
                    # z = z^2 + c
                    z = z * z
                    z = z + c
                    count += 1

                if count != self.iterations:
                    # Continuous coloring... https://www.paridebroggi.com/blogpost/2015/05/06/fractal-continuous-coloring/
                    continuous_index = count + 1 - (math.log(2) / abs(z)) / math.log(2)
                    r = int(math.sin(0.1 * continuous_index + 1) * 127.5 + 127.5)
                    g = int(math.sin(0.13 * continuous_index + 2) * 127.5 + 127.5)
                    b = int(math.sin(0.16 * continuous_index + 4) * 127.5 + 127.5)

                    canvas.set_pixel(x, y, (r, g, b))

        self.frame += 1

        if self.iterations < self.max_iterations:
            self.iterations += 1

        if self.frame > self.intro_time:
            self.scale *= 0.995
            self.center += (self.chosen_point - self.center) * (self.scale / 75)

        return False
