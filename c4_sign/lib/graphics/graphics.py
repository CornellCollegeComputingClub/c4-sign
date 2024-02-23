import numpy

from ..canvas import Canvas


def fill_screen(canvas: Canvas, color: int) -> None:
    """
    Sets the entire screen to the same color.

    :param canvas: The canvas to be colored.
    :param color: The color the canvas will be set to.
    :return: None.
    """
    for i in range(0, 1024):
        canvas.set_pixel(i % 32, i//32, color)


def clear_screen(canvas: Canvas) -> None:
    """
    Clears the screen. (Sets the entire screen to black).

    Note that new canvases are cleared by default when they are created.
    :param canvas: The canvas to clear.
    :return: None.
    """
    fill_screen(canvas, 0)


def stroke_line(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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



def __stroke_line_low(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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


def __stroke_line_high(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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


def __stroke_horizontal_line(canvas: Canvas, x1: int, x2: int, y: int, color: int) -> None:
    a = min(x1, x2)
    b = max(x1, x2)

    for i in range(a, b+1):
        canvas.set_pixel(i, y, color)


def stroke_rect(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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


def fill_rect(canvas: Canvas, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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

    for i in range(dx+1):
        for j in range(dy+1):
            canvas.set_pixel(x + i, y + j, color)

    pass


def stroke_ellipse(canvas: Canvas, cx: int, cy: int, rx: int, ry: int, color: int) -> None:
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

    d1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))

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

    d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))

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


def fill_ellipse(canvas: Canvas, cx: int, cy: int, rx: int, ry: int, color: int) -> None:
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

    d1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))

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

    d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))

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


def stroke_polyline(canvas: Canvas, points: list[tuple[int, int]], color: int) -> None:
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
        x2, y2 = points[i+1]
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


def draw_text(canvas: Canvas, text: str, x: int, y: int, color: int) -> None:
    """
    Draws the desired text on the screen at the appropriate x and y coordinates.
    :param canvas: The canvas to draw the text on.
    :param text: The text to draw on the canvas.
    :param x: The x-coordinate of the top left corner of the text.
    :param y: The y-coordinate of the top-left corner of the text.
    :param color: The color of the text.
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


if __name__ == "__main__":
    c = Canvas()

    fill_screen(c, (32, 0, 64))

    from PIL import Image
    import numpy
    card = numpy.asarray(Image.open("/home/mac/Downloads/MinecraftIconSmall.png").convert("RGBA"))

    # draw_image(c, 0, 0, bad_apple)
    draw_image(c, 24, -5, card)

    c.debug()
