from typing import Union

import bdfparser
import numpy

from .canvas import Canvas


def fill_screen(canvas: Canvas, color: Union[int, tuple[int, int, int]]) -> None:
    """
    Sets the entire screen to the same color.

    :param canvas: The canvas to be colored.
    :param color: The color the canvas will be set to.
    :return: None.
    """
    # for i in range(0, 1024):
    #     canvas.set_pixel(i % 32, i//32, color)
    # needs to be a tuple (r, g, b)
    if isinstance(color, int):
        r, g, b = (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF
        canvas.data[::][::] = (r, g, b)
    else:
        canvas.data[::][::] = color


def clear_screen(canvas: Canvas) -> None:
    """
    Clears the screen. (Sets the entire screen to black).

    Note that new canvases are cleared by default when they are created.
    :param canvas: The canvas to clear.
    :return: None.
    """
    fill_screen(canvas, 0)


def stroke_line(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Colors a line of pixels between one point and another.
    :param canvas: The canvas the line will be drawn on.
    :param x1: The x-coordinate of the first point.
    :param y1: The y-coordinate of the first point.
    :param x2: The x-coordinate of the second point.
    :param y2: The y-coordinate of the second point.
    :param color: The color the line will be given.
    :return: None.
    """

    # Bresenham's line algorithm: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

    if abs(y2 - y1) < abs(x2 - x1):
        if x1 > x2:
            __stroke_line_low(canvas, x2, y2, x1, y1, color)
        else:
            __stroke_line_low(canvas, x1, y1, x2, y2, color)
    else:
        if y1 > y2:
            __stroke_line_high(canvas, x2, y2, x1, y1, color)
        else:
            __stroke_line_high(canvas, x1, y1, x2, y2, color)


def __stroke_line_low(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    dx = x2 - x1
    dy = y2 - y1
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = (2 * dy) - dx
    y = y1

    for x in range(x1, x2):
        canvas.set_pixel(x, y, color)
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * dy


def __stroke_line_high(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    dx = x2 - x1
    dy = y2 - y1
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = (2 * dx) - dy
    x = x1

    for y in range(y1, y2):
        canvas.set_pixel(x, y, color)
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * dx


def __stroke_horizontal_line(canvas: Canvas, x1: int, x2: int, y: int, color: Union[int, tuple[int, int, int]]) -> None:
    a = min(x1, x2)
    b = max(x1, x2)

    for i in range(a, b + 1):
        canvas.set_pixel(i, y, color)


def stroke_rect(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Colors the edges of a rectangle whose corners are defined by two points.

    This function colors the edges of the rectangle. See fill_rect in order to fully color a rectangle.
    :param canvas: The canvas the rectangle will be drawn on.
    :param x1: The x-coordinate of the rectangle's top left corner.
    :param y1: The y-coordinate of the rectangle's top left corner.
    :param x2: The x-coordinate of the rectangle's bottom right corner.
    :param y2: The y-coordinate of the rectangle's bottom right corner.
    :param color: The color the rectangle will be colored.
    :return:
    """

    dx = abs(x2 - x1)
    x = min(x1, x2)

    dy = abs(y2 - y1)
    y = min(y1, y2)

    for i in range(x, x + dx + 1):
        canvas.set_pixel(i, y, color)

    for i in range(x, x + dx + 1):
        canvas.set_pixel(i, y + dy, color)

    for i in range(y + 1, y + dy):
        canvas.set_pixel(x, i, color)

    for i in range(y + 1, y + dy):
        canvas.set_pixel(x + dx, i, color)


def fill_rect(
    canvas: Canvas,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Colors the inside of a rectangle whose corners are defined by two points.

    This function colors the interior of the rectangle. See stroke_rect in order to color the edges.
    :param canvas: The canvas the rectangle will be drawn on.
    :param x1: The x-coordinate of the rectangle's top left corner.
    :param y1: The y-coordinate of the rectangle's top left corner.
    :param x2: The x-coordinate of the rectangle's bottom right corner.
    :param y2: The y-coordinate of the rectangle's bottom right corner.
    :param color: The color the rectangle will be colored.
    :return: None.
    """

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x = min(x1, x2)
    y = min(y1, y2)

    for i in range(dx + 1):
        for j in range(dy + 1):
            canvas.set_pixel(x + i, y + j, color)

    pass


def stroke_ellipse(
    canvas: Canvas,
    cx: int,
    cy: int,
    rx: int,
    ry: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Draws the outline of an ellipse on the canvas centered at (cx, cy).

    :param canvas: The canvas to draw on.
    :param cx: The x-coordinate of the center of the ellipse.
    :param cy: The y-coordinate of the center of the ellipse.
    :param rx: The radius of the ellipse in the x- direction.
    :param ry: The radius of the ellipse in the y- direction.
    :param color: The color of the ellipse.
    :return: None.
    """
    # Implementation of midpoint-ellipse algorithm: https://www.geeksforgeeks.org/midpoint-ellipse-drawing-algorithm/
    x = 0
    y = ry

    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)

    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    while dx < dy:
        canvas.set_pixel(x + cx, y + cy, color)
        canvas.set_pixel(-x + cx, y + cy, color)
        canvas.set_pixel(x + cx, -y + cy, color)
        canvas.set_pixel(-x + cx, -y + cy, color)

        # PLOT
        if d1 < 0:
            x += 1
            dx = dx + 2 * ry * ry
            d1 = d1 + dx + ry * ry
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)

    while y >= 0:
        canvas.set_pixel(x + cx, y + cy, color)
        canvas.set_pixel(-x + cx, y + cy, color)
        canvas.set_pixel(x + cx, -y + cy, color)
        canvas.set_pixel(-x + cx, -y + cy, color)

        if d2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)


def fill_ellipse(
    canvas: Canvas,
    cx: int,
    cy: int,
    rx: int,
    ry: int,
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Draws a filled ellipse on the canvas centered at (cx, cy).

    :param canvas: The canvas to draw on.
    :param cx: The x-coordinate of the center of the ellipse.
    :param cy: The y-coordinate of the center of the ellipse.
    :param rx: The radius of the ellipse in the x- direction.
    :param ry: The radius of the ellipse in the y- direction.
    :param color: The color of the ellipse.
    :return: None.
    """
    # Implementation of midpoint-ellipse algorithm: https://www.geeksforgeeks.org/midpoint-ellipse-drawing-algorithm/
    # See this stackoverflow link for discussion:
    # https://stackoverflow.com/questions/10878209/midpoint-circle-algorithm-for-filled-circles
    x = 0
    y = ry

    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)

    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    while dx < dy:
        __stroke_horizontal_line(canvas, -x + cx, x + cx, y + cy, color)
        __stroke_horizontal_line(canvas, -x + cx, x + cx, -y + cy, color)

        # PLOT
        if d1 < 0:
            x += 1
            dx = dx + 2 * ry * ry
            d1 = d1 + dx + ry * ry
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    d2 = ((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry)

    while y >= 0:
        __stroke_horizontal_line(canvas, x + cx, -x + cx, y + cy, color)
        __stroke_horizontal_line(canvas, x + cx, -x + cx, -y + cy, color)

        if d2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)


def stroke_circle(canvas: Canvas, x: int, y: int, radius: int, color: int) -> None:
    """
    Strokes the edge of a circle with a color.

    This function colors the edge of the circle. See fill_circle in order to fill the circle.
    :param canvas: The canvas to draw the circle on.
    :param x: The x-coordinate of the circle's center.
    :param y: The y-coordinate of the circle's center.
    :param radius: The radius of the circle.
    :param color: The color to draw the circle with.
    :return: None.
    """
    stroke_ellipse(canvas, x, y, radius, radius, color)


def fill_circle(canvas: Canvas, x: int, y: int, radius: int, color: int) -> None:
    """
    Fills a circle with a color.

    This function colors the interior of the circle. See stroke_circle in order to draw the edges.
    :param canvas: The canvas to draw the circle on.
    :param x: The x-coordinate of the circle's center.
    :param y: The y-coordinate of the circle's center.
    :param radius: The radius of the circle.
    :param color: The color to draw the circle with.
    :return: None.
    """
    fill_ellipse(canvas, x, y, radius, radius, color)


def stroke_polyline(
    canvas: Canvas,
    points: list[tuple[int, int]],
    color: Union[int, tuple[int, int, int]],
) -> None:
    """
    Colors a sequence of lines, making a path.

    To fill a path, see fill_polygon.
    :param canvas: The canvas to draw the lines on.
    :param points: A list of points, represented by tuples whose elements are the x- and y-coordinates of each point.
    :param color: The color to draw the lines with.
    :return: None.
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        stroke_line(canvas, x1, y1, x2, y2, color)


def fill_polygon(canvas: Canvas, points: list[tuple[int, int]], color: int) -> None:
    """
    Fills the interior of a polygon with the desired color.

    To fill a path, see fill_polygon.
    :param canvas: The canvas to draw the polygon on.
    :param points: A list of points, represented by tuples whose elements are the x- and y-coordinates of each point.
    :param color: The color to fill the polygon with.
    :return: None.
    """
    pass


def draw_image(canvas: Canvas, top_left_x: int, top_left_y: int, image: numpy.ndarray) -> None:
    """
    Draws an image on the canvas. Useful for "sprites", photos, and other graphics!

    :param canvas: The canvas to draw the image on.
    :param top_left_x: The x-coordinate of the top left corner of the image.
    :param top_left_y: The y-coordinate of the top left corner of the image.
    :param image: The image to draw.
    :return: None
    """

    width, height, depth = image.shape

    tly = min(32, max(0, top_left_y))
    tlx = min(32, max(0, top_left_x))
    bry = min(32, max(0, top_left_y + height))
    brx = min(32, max(0, top_left_x + width))

    for y in range(tly, bry):
        for x in range(tlx, brx):
            source_y = y - top_left_y
            source_x = x - top_left_x
            alpha = 1 if depth == 3 else (image[source_y][source_x][3] / 255)
            r = int((1 - alpha) * canvas.data[y][x][0] + alpha * image[source_y][source_x][0])
            g = int((1 - alpha) * canvas.data[y][x][1] + alpha * image[source_y][source_x][1])
            b = int((1 - alpha) * canvas.data[y][x][2] + alpha * image[source_y][source_x][2])

            # Shhhhhhh....
            canvas.data[y][x] = (r, g, b)


class Font:
    def __init__(self, path):
        self.bdf_font = bdfparser.Font(path)
        self.headers = self.bdf_font.headers
        self.props = self.bdf_font.props
        self.default_char = self.bdf_font.glyphbycp(0xFFFD)

    def character_width(self, char: int):
        # Missing glyphs return 0 width in rpi-rgb-led-matrix
        # since i want things to be consistent, i'll do the same
        if not self.bdf_font.glyphbycp(char):
            return 0

        return self.bdf_font.glyphbycp(char).meta["dwx0"]

    @property
    def height(self):
        return self.headers["fbby"]

    @property
    def width(self):
        return self.headers["fbax"]

    @property
    def baseline(self):
        return self.headers["fbby"] + self.headers["fbbyoff"]


def draw_text(canvas: Canvas, font: Font, x: int, y: int, color: Union[int, tuple[int, int, int]], text: str) -> None:
    """
    Draws the desired text on the screen at the appropriate x and y coordinates.
    :param canvas: The canvas to draw the text on.
    :param font: The font to use for the text.
    :param x: The x-coordinate of the bottom left corner of the text.
    :param y: The y-coordinate of the bottom left corner of the text.
    :param color: The color of the text.
    :param text: The text to draw on the canvas.
    :return: None.
    """
    if len(text) == 0:
        return  # nothing to draw!

    # Support multiple spacings based on device width
    character_widths = [__actual_char_width(font, letter) for letter in text]
    first_char_width = character_widths[0]
    max_char_width = max(character_widths)
    total_width = sum(character_widths)

    # Offscreen to the left, adjust by first character width
    if x < 0:
        adjustment = abs(x + first_char_width) // first_char_width
        text = text[adjustment:]
        if adjustment:
            x += first_char_width * adjustment

    # Offscreen to the right, rough adjustment by max width
    if (total_width + x) > canvas.width:
        text = text[: ((canvas.width + 1) // max_char_width) + 2]

    # Draw the text!
    if len(text) != 0:
        # Ensure text doesn't get drawn as multiple lines
        linelimit = len(text) * (font.headers["fbbx"] + 1)

        text_map = font.bdf_font.draw(text, linelimit, missing=font.default_char).todata(2)
        font_y_offset = -(font.headers["fbby"] + font.headers["fbbyoff"])

        for y2, row in enumerate(text_map):
            for x2, value in enumerate(row):
                if value == 1:
                    canvas.set_pixel(x + x2, y + y2 + font_y_offset, color)

    return total_width


def __actual_char_width(font: Font, char: str) -> int:
    width = font.character_width(ord(char))

    if width > 0:
        return width

    return font.character_width(font.default_char.cp())


if __name__ == "__main__":
    c = Canvas()

    from c4_sign.consts import FONT_4x6 as f

    draw_text(c, f, 0, 10, (255, 255, 255), "hello :3")

    c.debug()
