import math
from dataclasses import dataclass
from datetime import timedelta

from c4_sign.base_task import OptimScreenTask
from c4_sign.lib.canvas import Canvas


class JuliaSet(OptimScreenTask):
    title = "Julia Sets"
    artist = "Mac Coleman"

    def prepare(self):
        self.angle = 0
        self.angular_velocity = math.pi / (128)
        self.center = complex(0, 0)
        self.c = complex(0.751, 0)
        self.scale = 4
        self.frame = 0
        self.iterations = 1
        self.max_iterations = 150
        self.epic_colors = [
            0xFF0000,
            0xFF6000,
            0xFFBF00,
            0xB5FF00,
            0x80FF00,
            0x20FF00,
            0x00FF40,
            0x00FFFF,
            0x009FFF,
            0x0040FF,
            0x2000FF,
            0x7F00FF,
            0xDF00FF,
            0xFF00BF,
            0xFF0060,
        ]
        return super().prepare()

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

                z = complex(u, v)

                count = 0
                while abs(z) ** 2 < 4.0 and count < self.iterations:
                    # z = z^2 + c
                    z **= 2
                    z += self.c
                    count += 1

                if count != self.iterations:
                    canvas.set_pixel(x, y, self.epic_colors[count % len(self.epic_colors)])

        self.frame += 1

        if self.iterations < self.max_iterations:
            self.iterations += 1

        # Sweep seed point around outside of main cardioid
        self.angle += self.angular_velocity
        self.c = complex(1.1 * math.cos(self.angle), 1.1 * math.sin(self.angle))

        return True
