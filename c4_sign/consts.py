try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics
from pkg_resources import resource_filename


DEV_MODE = False
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_RED = graphics.Color(255, 69, 58)
COLOR_ORANGE = graphics.Color(255, 159, 10)
COLOR_YELLOW = graphics.Color(255, 214, 10)
COLOR_GREEN = graphics.Color(50, 215, 75)
COLOR_MINT = graphics.Color(102, 212, 207)
COLOR_TEAL = graphics.Color(106, 196, 220)
COLOR_CYAN = graphics.Color(90, 200, 245)
COLOR_BLUE = graphics.Color(10, 132, 255)
COLOR_INDIGO = graphics.Color(94, 92, 230)
COLOR_PURPLE = graphics.Color(191, 90, 242)
COLOR_PINK = graphics.Color(255, 55, 95)
COLOR_BROWN = graphics.Color(172, 142, 104)
COLOR_GRAY = graphics.Color(152, 152, 157)
FONT_4x6 = graphics.Font()
FONT_4x6.LoadFont(resource_filename(__name__, "fonts/4x6.bdf"))
FONT_5x7 = graphics.Font()
FONT_5x7.LoadFont(resource_filename(__name__, "fonts/5x7.bdf"))
FONT_9x15 = graphics.Font()
FONT_9x15.LoadFont(resource_filename(__name__, "fonts/9x15.bdf"))