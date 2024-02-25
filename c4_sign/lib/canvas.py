from typing import Union

import numpy


class Canvas:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.data = numpy.zeros((self.height, self.width, 3), dtype=numpy.uint8)

    def get_pixel(self, x: int, y: int):
        return self.data[y][x]

    def set_pixel(self, x: int, y: int, color: Union[int, tuple[int, int, int], tuple[int, int, int, int]]):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return  # Just ignore mistakes

        if isinstance(color, tuple):
            if len(color) == 3:
                self.data[y][x] = color
            else:
                br, bg, bb = self.data[y][x]
                a = color[3] / 255
                r = int(color[0] * (1 - a) + br * a)
                g = int(color[1] * (1 - a) + bg * a)
                b = int(color[2] * (1 - a) + bb * a)
                self.data[y][x] = (r, g, b)
        else:
            # 0xabcdef
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            self.data[y][x] = (r, g, b)

    def clear(self):
        self.data.fill(0)

    def tolist(self):
        # [0xRRGGBB, 0xRRGGBB, ...]
        pass

    def serialize(self):
        return self.data.tolist()

    def __getitem__(self, key):
        y, x = (key // self.width, key % self.width)
        r, g, b = self.data[y][x]
        return int((r << 16) | (g << 8) | b)

    def tobytes(self):
        return self.data.tobytes()

    def debug(self) -> None:
        for y in range(0, self.height, 2):
            for x in range(self.width):
                # Prepare top pixel (background)
                top_r, top_g, top_b = self.data[y][x]
                print(f"\033[48;2;{top_r};{top_g};{top_b}m", end="")
                # Prepare bottom pixel (foreground)
                bottom_r, bottom_g, bottom_b = self.data[y + 1][x]
                print(f"\033[38;2;{bottom_r};{bottom_g};{bottom_b}m", end="")

                # Print the actual pixels.
                print("▄", end="")

            print("\033[0m")  # Reset colors
