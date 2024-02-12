import numpy

class Canvas:
    def __init__(self):
        self.width = 32
        self.height = 32
        self.data = numpy.zeros((self.height, self.width, 3), dtype=numpy.uint8)
    
    def get_pixel(self, x: int, y: int):
        return self.data[y][x]
    
    def set_pixel(self, x: int, y: int, color: tuple | int):
        if isinstance(color, tuple):
            self.data[y][x] = color
        else:
            # 0xabcdef
            r = (color >> 16) & 0xff
            g = (color >> 8) & 0xff
            b = color & 0xff
            self.data[y][x] = (r, g, b)

    def tolist(self):
        return self.data.tolist()
    
    def tobytes(self):
        return self.data.tobytes()

    def debug(self) -> None:
        for y in range(0, self.height, 2):
            for x in range(self.width):
                # Prepare top pixel (background)
                top_r, top_g, top_b = self.data[y][x]
                print(f"\033[48;2;{top_r};{top_g};{top_b}m", end="")
                # Prepare bottom pixel (foreground)
                bottom_r, bottom_g, bottom_b = self.data[y+1][x]
                print(f"\033[38;2;{bottom_r};{bottom_g};{bottom_b}m", end="")

                # Print the actual pixels.
                print("▄", end="")

            print("\033[0m") # Reset colors
