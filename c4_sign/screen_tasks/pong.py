import math
import random
from datetime import timedelta

from c4_sign.base_task import ScreenTask
from c4_sign.consts import FONT_4x6
from c4_sign.lib.canvas import Canvas
from c4_sign.lib.graphics import draw_text, fill_rect


class Pong(ScreenTask):
    title = "Pong"
    artist = "Mac Coleman"

    def prepare(self):
        self.frame = 0
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
        self.paddle_height = 8
        self.left_paddle_y = 16
        self.right_paddle_y = 16

        self.left_score = 0
        self.right_score = 0

        self.ball_x, self.ball_y = 16.0, 16.0
        angle = (random.random() * math.pi / 2 - math.pi / 4) * 0.3
        self.ball_vel_x, self.ball_vel_y = 20 * math.cos(angle), 20 * math.sin(angle)

        self.last_points = []
        self.last_left_paddle = []
        self.last_right_paddle = []

        return super().prepare()

    def draw_frame(self, canvas: Canvas, delta_time: timedelta) -> bool:
        self.ball_x += self.ball_vel_x * delta_time.total_seconds()
        self.ball_y += self.ball_vel_y * delta_time.total_seconds()

        left_dist = self.ball_y - self.left_paddle_y
        right_dist = self.ball_y - self.right_paddle_y

        left_paddle_vel = left_dist / abs(left_dist) / 1.5 if abs(left_dist) > 3 else 0
        right_paddle_vel = right_dist / abs(right_dist) / 1.5 if abs(right_dist) > 3 else 0

        if self.ball_vel_x > 0:
            left_paddle_vel /= 10
        else:
            right_paddle_vel /= 10

        self.left_paddle_y += left_paddle_vel
        self.right_paddle_y += right_paddle_vel

        # Worst line rasterization ''''''algorithm'''''' known to humanity
        last_colored = None
        color_index = 0
        for i, v in reversed(list(enumerate(self.last_points))):
            if i - 1 < 0 or color_index > len(self.epic_colors):
                break
            f = list(self.last_points[i][:])
            l = self.last_points[i - 1]
            step_x = 0.25 * (l[0] - f[0]) / math.sqrt((l[0] - f[0]) ** 2 + (l[1] - f[1]) ** 2)
            step_y = 0.25 * (l[1] - f[1]) / math.sqrt((l[0] - f[0]) ** 2 + (l[1] - f[1]) ** 2)
            while (l[0] - f[0]) ** 2 + (l[1] - f[1]) ** 2 > 0.25:
                f[0] += step_x
                f[1] += step_y
                if (int(f[0]), int(f[1])) != last_colored:
                    c = self.epic_colors[color_index % len(self.epic_colors)]
                    r = c >> 16
                    g = (c >> 8) & 0xFF
                    b = c & 0xFF
                    canvas.set_pixel(
                        int(f[0]), int(f[1]), (r, g, b, min(255, int(255 * color_index / len(self.epic_colors))))
                    )
                    color_index += 1
                    last_colored = (int(f[0]), int(f[1]))

        canvas.set_pixel(int(self.ball_x), int(self.ball_y), 0xFFFFFF)

        last_left = int(self.left_paddle_y)
        color_index = 0
        for i, point in enumerate(self.last_left_paddle):
            if int(point) == last_left:
                continue
            c = self.epic_colors[color_index % len(self.epic_colors)]
            r = c >> 16
            g = (c >> 8) & 0xFF
            b = c & 0xFF
            fill_rect(
                canvas,
                2,
                int(point + self.paddle_height / 2),
                2,
                int(point - self.paddle_height / 2),
                (r, g, b, min(255, int(255 * (len(self.epic_colors) - i) / len(self.epic_colors)))),
            )
            last_left = int(point)
            color_index += 1

        last_right = int(self.right_paddle_y)
        color_index = 0
        for i, point in enumerate(self.last_right_paddle):
            if int(point) == last_right:
                continue
            c = self.epic_colors[color_index % len(self.epic_colors)]
            r = c >> 16
            g = (c >> 8) & 0xFF
            b = c & 0xFF
            fill_rect(
                canvas,
                29,
                int(point + self.paddle_height / 2),
                29,
                int(point - self.paddle_height / 2),
                (r, g, b, min(255, int(255 * (len(self.epic_colors) - i) / len(self.epic_colors)))),
            )
            last_right = int(point)
            color_index += 1

        fill_rect(
            canvas,
            2,
            int(self.left_paddle_y + self.paddle_height / 2),
            2,
            int(self.left_paddle_y - self.paddle_height / 2),
            0xFFFFFF,
        )

        fill_rect(
            canvas,
            29,
            int(self.right_paddle_y + self.paddle_height / 2),
            29,
            int(self.right_paddle_y - self.paddle_height / 2),
            0xFFFFFF,
        )

        draw_text(canvas, FONT_4x6, 9, 6, 0xFFFFFF, str(self.left_score))
        draw_text(canvas, FONT_4x6, 20, 6, 0xFFFFFF, str(self.right_score))

        if self.ball_x >= 32 or self.ball_x <= 0:
            self.ball_vel_x *= -1

        if self.ball_x >= 29 and self.ball_vel_x > 0:
            if abs(right_dist) < math.ceil(self.paddle_height / 2) + 1:
                self.ball_vel_x *= -1
                self.ball_vel_y += right_dist
            else:
                self.left_score += 1
                self.ball_x, self.ball_y = 16.0, 16.0
                angle = (random.random() * math.pi / 2 - math.pi / 4) * 0.3
                self.ball_vel_x, self.ball_vel_y = 20 * math.cos(angle), 20 * math.sin(angle)
                self.last_points = []

        if self.ball_x < 3 and self.ball_vel_x < 0:
            if abs(left_dist) < math.ceil(self.paddle_height / 2) + 1:
                self.ball_vel_x *= -1
                self.ball_vel_y += left_dist
            else:
                self.right_score += 1
                self.ball_x, self.ball_y = 16.0, 16.0
                angle = (random.random() * math.pi / 2 - math.pi / 4) * 0.3
                self.ball_vel_x, self.ball_vel_y = -20 * math.cos(angle), 20 * math.sin(angle)
                self.last_points = []

        self.ball_vel_y = min(20.0, max(self.ball_vel_y, -20.0))

        if (self.ball_y >= 32 and self.ball_vel_y > 0) or (self.ball_y <= 0 and self.ball_vel_y < 0):
            self.ball_vel_y *= -1

        self.last_points.append((self.ball_x, self.ball_y))

        if len(self.last_left_paddle) > len(self.epic_colors):
            self.last_left_paddle.pop(0)

        if len(self.last_right_paddle) > len(self.epic_colors):
            self.last_right_paddle.pop(0)

        self.last_left_paddle.append(self.left_paddle_y)
        self.last_right_paddle.append(self.right_paddle_y)

        return False
