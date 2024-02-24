from pkg_resources import resource_filename

from c4_sign.lib import graphics

DEV_MODE = False
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 69, 58)
COLOR_ORANGE = (255, 159, 10)
COLOR_YELLOW = (255, 214, 10)
COLOR_GREEN = (50, 215, 75)
COLOR_MINT = (102, 212, 207)
COLOR_TEAL = (106, 196, 220)
COLOR_CYAN = (90, 200, 245)
COLOR_BLUE = (10, 132, 255)
COLOR_INDIGO = (94, 92, 230)
COLOR_PURPLE = (191, 90, 242)
COLOR_PINK = (255, 55, 95)
COLOR_BROWN = (172, 142, 104)
COLOR_GRAY = (152, 152, 157)
FONT_4x6 = graphics.Font(resource_filename(__name__, "fonts/4x6.bdf"))
FONT_5x7 = graphics.Font(resource_filename(__name__, "fonts/5x7.bdf"))
FONT_9x15 = graphics.Font(resource_filename(__name__, "fonts/9x15.bdf"))
