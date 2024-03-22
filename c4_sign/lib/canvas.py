from pathlib import Path
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
            # note: we cannot pass a 0xRRGGBBAA color directly. if there is no red, the GBA will be interpreted as RGB.
            # so, i'm making alpha be the first bit, and then the rest is the color. (0xAARRGGBB)
            a = (color >> 24) & 0xFF
            if a == 0:
                # we can only assume that if the alpha is 0, it's in the format 0xRRGGBB
                # and, therefore, it should be fully opaque.
                # if this is not the case, the user should use the tuple format.
                # (or, better yet, not call this because it's fully transparent and it's a waste of time.)
                a = 255
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            # handle alpha
            br, bg, bb = self.data[y][x]
            a /= 255
            r = int(r * a + br * (1 - a))
            g = int(g * a + bg * (1 - a))
            b = int(b * a + bb * (1 - a))
            self.data[y][x] = (r, g, b)

    def clear(self):
        self.data.fill(0)

    def serialize(self):
        return self.data.tolist()
    
    def fixup(self):
        # ensure that self.data[y][x] is a tuple of (r, g, b)
        for y in range(self.height):
            for x in range(self.width):
                if not isinstance(self.data[y][x], tuple):
                    # print(f"Fixing up pixel at {x}, {y}", self.data[y][x])
                    self.data[y][x] = tuple(self.data[y][x])


    def __getitem__(self, key):
        y, x = (key // self.width, key % self.width)
        r, g, b = self.data[y][x]
        return r, g, b

    def tobytes(self):
        return self.data.tobytes()

    def to_jpg(self, path: Union[str, Path], size_multiplier=8.0) -> None:
        from PIL import Image

        img = Image.fromarray(self.data, "RGB")
        img = img.resize((int(self.width * size_multiplier), int(self.height * size_multiplier)), Image.NEAREST)
        img.save(path)

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
