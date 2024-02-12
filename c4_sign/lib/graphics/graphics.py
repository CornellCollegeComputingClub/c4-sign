from ..canvas import Canvas


def fill_screen(canvas: any, color: int | tuple[int, int, int]) -> None:
    """
    Sets the entire screen to the same color.

    :param canvas: The canvas to be colored.
    :param color: The color the canvas will be set to.
    :return: None.
    """
    for i in range(0, 1024):
        canvas.set_pixel(i % 32, i//32, color)


def clear_screen(canvas: any) -> None:
    """
    Clears the screen. (Sets the entire screen to black).

    Note that new canvases are cleared by default when they are created.
    :param canvas: The canvas to clear.
    :return: None.
    """
    fill_screen(canvas, 0)


def stroke_line(canvas: any, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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
    pass


def stroke_rect(canvas: any, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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
    pass


def fill_rect(canvas: any, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
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
    pass


def stroke_circle(canvas: any, x: int, y: int, radius: int, color: int) -> None:
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
    pass


def fill_circle(canvas: any, x: int, y: int, radius: int, color: int) -> None:
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
    pass


def stroke_polyline(canvas: any, points: list[tuple[int, int]], color: int) -> None:
    """
    Colors a sequence of lines, making a path.

    To fill a path, see fill_polygon.
    :param canvas: The canvas to draw the lines on.
    :param points: A list of points, represented by tuples whose elements are the x- and y-coordinates of each point.
    :param color: The color to draw the lines with.
    :return: None.
    """
    pass


def fill_polygon(canvas: any, points: list[tuple[int, int]], color: int) -> None:
    """
    Fills the interior of a polygon with the desired color.

    To fill a path, see fill_polygon.
    :param canvas: The canvas to draw the polygon on.
    :param points: A list of points, represented by tuples whose elements are the x- and y-coordinates of each point.
    :param color: The color to fill the polygon with.
    :return: None.
    """
    pass


def draw_text(canvas: any, text: str, x: int, y: int, color: int) -> None:
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


def draw_image(canvas: any, top_left_x: int, top_left_y: int, image) -> None:
    """
    Draws an image on the canvas. Useful for "sprites", photos, and other graphics!

    :param canvas: The canvas to draw the image on.
    :param top_left_x: The x-coordinate of the top left corner of the image.
    :param top_left_y: The y-coordinate of the top left corner of the image.
    :param image: The image to draw.
    :return:
    """
    pass

c = Canvas()

c.debug()