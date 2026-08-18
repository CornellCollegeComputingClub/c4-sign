from rpi_ws281x import PixelStrip, Color
import numpy
import argparse
from c4_sign.lib.screen.physical.driver import lcd
from c4_sign.lib.graphics import __actual_char_width
from c4_sign.consts import FONT_4x6

def draw_centered_text(array, text, font, color, y):
    character_widths = [__actual_char_width(font, letter) for letter in text]
    first_char_width = character_widths[0]
    max_char_width = max(character_widths)
    total_width = sum(character_widths)

    x = (32 - total_width) // 2

    # Offscreen to the left, adjust by first character width
    if x < 0:
        adjustment = abs(x + first_char_width) // first_char_width
        text = text[adjustment:]
        if adjustment:
            x += first_char_width * adjustment

    # Offscreen to the right, rough adjustment by max width
    if (total_width + x) > 32:
        text = text[: ((32 + 1) // max_char_width) + 2]

    # Draw the text!
    if len(text) != 0:
        # Ensure text doesn't get drawn as multiple lines
        linelimit = len(text) * (font.headers["fbbx"] + 1)

        text_map = font.bdf_font.draw(text, linelimit, missing=font.default_char).todata(2)
        font_y_offset = -(font.headers["fbby"] + font.headers["fbbyoff"])

        for y2, row in enumerate(text_map):
            for x2, value in enumerate(row):
                if value == 1:
                    array[x+x2][y+y2+font_y_offset] = color

parser = argparse.ArgumentParser(prog="Message", description="Display a message on the screen and LCD")
parser.add_argument("textline1")
parser.add_argument("textline2")
parser.add_argument("-c", "--color")

lcd_screen = lcd()
pixels = PixelStrip(1024, 18, 800000, 10, False, 255, 0)
pixels.begin()

quadrant_one = []

# Generate the zigzag for one quadrant.
for i in range(0, 8):
    row1, row2 = [], []
    for j in range(15, -1, -1):
        row1.append(i * 32 + j)

    for j in range(0, 16):
        row2.append((i * 32) + 16 + j)

    quadrant_one.append(row1)
    quadrant_one.append(row2)

# Add constant offset to all four quadrants.
from copy import deepcopy

top_right = quadrant_one
top_left = [[y + 256 for y in x] for x in deepcopy(quadrant_one)]
bot_right = [[y + 512 for y in x] for x in deepcopy(quadrant_one)]
bot_left = [[y + 768 for y in x] for x in deepcopy(quadrant_one)]

for i, x in enumerate(top_left):
    x.extend(top_right[i])

for i, x in enumerate(bot_left):
    x.extend(bot_right[i])

top_left.extend(bot_left)

address_table = numpy.argsort(numpy.array(top_left).reshape(1024))


canvas = numpy.zeros((32, 32, 3), dtype=numpy.uint8)


args = parser.parse_args()


color = [255, 255, 255]
if args.color is not None:
    color = [int(args.color[1:3], 16), int(args.color[3:5], 16), int(args.color[5:7], 16)]


draw_centered_text(canvas, args.textline1, FONT_4x6, color, 15)
draw_centered_text(canvas, args.textline2, FONT_4x6, color, 16 + 7)


gamma = 2.8 # Who knows if this'll look nice at all
m_in = 255
m_out = int(0.15 * 255)

a = canvas.astype(numpy.float32)
a /= m_in
a **= gamma
a *= m_out
a += 0.5
a = a.astype(numpy.uint8)


f = lambda c: Color(int(c[0]), int(c[1]), int(c[2]))
colors = list(map(f, a.reshape((1024, 3))[address_table]))
for i in range(1024):
    pixels[i] = colors[i]

pixels.show()

lcd.lcd_display_string(args.textline1, 1)
lcd.lcd_display_string(args.textline2, 2)

