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
