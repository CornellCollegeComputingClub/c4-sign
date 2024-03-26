import math
import random
from dataclasses import dataclass
from datetime import timedelta

from c4_sign.base_task import OptimScreenTask
from c4_sign.lib.canvas import Canvas


@dataclass
class Complex:
    real: float
    imag: float

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        if isinstance(other, float) or isinstance(other, int):
            return Complex(self.real + other, self.imag)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        if isinstance(other, float) or isinstance(other, int):
            return Complex(self.real - other, self.imag)

    def __mul__(self, other):
        # (a + bi) * (c + di)
        # a*c + a*di + b*ci + b*d*ii
        # a*c + a*di + b*ci - b*d
        # (a*c - b*d) + (a*d + b*c)i
        if isinstance(other, Complex):
            r = self.real * other.real - self.imag * other.imag
            i = self.real * other.imag + self.imag * other.real
            return Complex(r, i)
        elif isinstance(other, float) or isinstance(other, int):
            return Complex(self.real * other, self.imag * other)
        else:
            raise TypeError("Expected float or Complex.")

    def mag_squared(self):
        return self.real**2 + self.imag**2


class BurningShip(OptimScreenTask):
    title = "Burning Ship"
    artist = "Mac Coleman"
    ignore = True

    def prepare(self):
        self.center = Complex(0, 0)
        self.scale = 4
        self.frame = 0
        self.iterations = 1
        self.max_iterations = 30
        self.intro_time = 140
        self.epic_points = [
            Complex(-(1.7721983880271375 + 1.7722187032801162) / 2, -(0.04251487432886503 + 0.04254394619090975) / 2),
            Complex(-(-0.8379819119999999 + -0.83577771) / 2, -(1.4488082728234664 + 1.4510926572533736) / 2),
            Complex(-(1.8613924060088474 + 1.861552262730194) / 2, -(0.0019904228838272166 + 0.002072016456434031) / 2),
            Complex(-(0.8194765540832001 + 0.8196362197226658) / 2, -(0.9403571999704258 + 0.9405396096087764) / 2),
            Complex(-(1.7730901168969844 + 1.7730901168969884) / 2, -(0.0657946834733513 + 0.06579468347335482) / 2),
        ]
        self.chosen_point = None
        return super().prepare()

    def get_lcd_text(self) -> str:
        mrt = self.max_run_time.total_seconds()
        et = self.elapsed_time.total_seconds()
        if self.frame < self.intro_time or mrt - et < 5.0:
            return super().get_lcd_text()

        if 20 < et < 40:
            return "very free".center(16) + "and easy".center(16)
        elif 40 <= et:
            return f"a = {self.chosen_point.real:12.8f}".center(16) + f" + {self.chosen_point.imag:12.8f}i".center(16)
        else:
            return "Burning ship".center(16) + "on the water...".center(16)

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

                z = Complex(0, 0)
                c = Complex(u, v)

                count = 0
                while z.mag_squared() < 4.0 and count < self.iterations:
                    # z = (|Re(z)| + i|Im(z)|)^2 + c
                    r = abs(z.real)
                    i = abs(z.imag)
                    z = Complex(r, i) * Complex(r, i)
                    z = z + c
                    count += 1

                if count != self.iterations:
                    # Continuous coloring... https://www.paridebroggi.com/blogpost/2015/05/06/fractal-continuous-coloring/
                    continuous_index = count + 1 - (math.log(2) / math.sqrt(z.mag_squared())) / math.log(2)
                    r = int(math.sin(0.1 * continuous_index + 1) * 127.5 + 127.5)
                    g = int(math.sin(0.13 * continuous_index + 2) * 30 + 30)
                    b = int(math.sin(0.16 * continuous_index + 4) * 127.5 + 127.5)

                    canvas.set_pixel(x, y, (r, g, b))

        self.frame += 1

        if self.iterations < self.max_iterations:
            self.iterations += 1

        if self.frame > self.intro_time and self.chosen_point is None:
            self.chosen_point = random.choice(self.epic_points)

        if self.frame > self.intro_time:
            self.scale *= 0.995
            self.center += (self.chosen_point - self.center) * (self.scale / 75)

        return False
