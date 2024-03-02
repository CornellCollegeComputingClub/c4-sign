# C4 Canvas Graphics API
This guide explains each of the functions in the graphics API that you can use to write your display programs.
If you are looking to learn how to write a basic display program, see the tutorial. INSERT LINK HERE.

Each display program must produce "frames" for the screen to display.
These frames are represented by `Canvas` objects that abstract the operations done on the screen.
This guide will go into detail on each of the operations available for `Canvas` objects to draw your display.

**To use any of the functions in this library, you must import the graphics library in your task**, like so:

```python
from c4_sign.lib import graphics

# additionally, importing the constants module is recommended
# this inculudes some pre-defined colors and fonts
from c4_sign import consts
```

# Table of Contents

1. [Datatypes](#datatypes)
   1. [Canvas](#canvas)
      1. [set_pixel](#set_pixel)
   1. [Color](#color)
   1. [Font](#font)
2. [Graphics Library](#graphlib)
   1. [fill_screen](#fill_screen)
   2. [clear_screen](#clear_screen)
   3. [stroke_line](#stroke_line)
   4. [stroke_rect](#stroke_rect)
   5. [fill_rect](#fill_rect)
   6. [stroke_ellipse](#stroke_ellipse)
   7. [fill_ellipse](#fill_ellipse)
   8. [stroke_circle](#stroke_circle)
   9. [fill_circle](#fill_circle)
   10. [stroke_polyline](#stroke_polyline)
   11. [fill_polygon](#fill_polygon)
   12. [draw_image](#draw_image)
   13. [draw_text](#draw_text)

## Datatypes <a name="datatypes"></a>

### Canvas <a name="canvas"></a>
The `Canvas` class is what you use to draw images on the LED screen!
As mentioned in the screen task tutorial, an empty canvas is given to the screen task to begin drawing the frame on.

The canvas is a direct representation of the LED screen: it is an interface for a 32 by 32 grid of cells in which colors can be stored.
The canvas has exactly one method that can be used to change how it displays:

#### Canvas.set_pixel(x, y, color) <a name="set_pixel"></a>
Changes the color of the pixel at the specified x,y position.

| Argument | Datatype  | Description                    |
|----------|-----------|--------------------------------|
| x        | `int`     | X-position of pixel to color   |
| y        | `int`     | Y-position of pixel to color   |
| color    | `Color`   | The color to set the pixel to. |

It should be noted that the pixel at x=0 and y=0 is the top-left corner of the screen.
This is standard for many graphics applications.
Also, note that because (0,0) is the top left, and the screen is 32x32 pixels, the highest x or y value you can use is 31.
If you call set_pixel with an x or y that falls outside of the range 0-31, no error will be produced, but also nothing will happen on the screen.

#### Examples
```python
# Set the pixel in the top left corner to red.
canvas.set_pixel(0,0, (255, 0, 0))

# Set the pixel in the top right corner to blue.
canvas.set_pixel(31, 0, consts.COLOR_BLUE)

# Set the pixel in the bottom right corner to white.
canvas.set_pixel(31, 31, 0xffffff)
```

The output of the following code is illustrated below:

![Canvas Example](./images/canvas_example.jpg)
### Color <a name="color"></a>
The color datatype is a type alias used to construct colors within your display programs.

```python
Color = Union[int, tuple[int, int, int], tuple[int, int, int, int]]
```

This means that color can either be represented as an `int` or as a `tuple` of three or four `int`s.

`tuple`s of three `int`s are treated as Red-Green-Blue color vectors, with each component in the range 0 to 255.
`tuple`s of four `int`s are treated as Red-Green-Blue-Alpha color vectors, with the extra alpha component representing
the "opacity" of the new color.
`int`s are again treated as Red-Green-Blue-Alpha color vectors. To represent a color as an int, write its components
in hexadecimal in the RGBA order. This format is common with HTML color pickers.

Any function that deals with `Color` as the input type can take any of these forms and display it correctly.

#### Examples
```python
# Solid colors as tuples
red = (255, 0, 0)
blue = (0, 0, 255)
greenish_yellow = (200, 250, 0)

# Transparent colors as tuples
transparent_green = (0, 255, 0, 128)
transparent_dark_blue = (0, 30, 128, 30)

# Colors as Integers
solid_white = 0xffffff
transparent_yellow = 0xff9000aa
```

#### A note on Alpha
Alpha ranges between 0 and 255 just like the other color components.
A color with alpha value `0` is fully opaque, while a color value with alpha `255` is fully transparent.
An example of using code with alpha is shown below:

```python
transparent_magenta = (255, 0, 255, 128)
transparent_cyan = (0, 255, 255, 128)
graphics.fill_rect(canvas, 0, 0, 21, 21, transparent_magenta)
graphics.fill_rect(canvas, 10, 10, 31, 31, transparent_cyan)
```
The above code will produce an image like this in the canvas:

![Transparency Example](./images/transparency.jpg)

### Font <a name="font"></a>

## Graphics Library <a name="graphlib"></a>
The graphics library contains methods to help you draw images on your screen!
It includes helper functions that can, for example, color the entire screen one color, draw lines or circles, and much more.

### `fill_screen(canvas, color)` <a name="fill_screen"></a>

Fills the canvas with the specified color.

| Argument | Datatype | Description                     |
|----------|----------|---------------------------------|
| canvas   | `Canvas` | The canvas to fill with color.  |
| color    | `Color`  | The color to set the canvas to. |

### `clear_screen(canvas)` <a name="clear_screen"></a>

Sets the entire canvas to black.

| Argument | Datatype | Description          |
|----------|----------|----------------------|
| canvas   | `Canvas` | The canvas to clear. |

### `stroke_line(canvas, x1, y1, x2, y2, color)` <a name="stroke_line"></a>

Draws a line between the points (x1, y1) and (x2, y2) with the specified color.

| Argument | Datatype | Description                                    |
|----------|----------|------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the line on.                |
| x1       | `int`    | The x-coordinate of one end of the line.       |
| y1       | `int`    | The y-coordinate of one end of the line.       |
| x2       | `int`    | The x-coordinate of the other end of the line. |
| y2       | `int`    | The y-coordinate of the other of the line.     |
| color    | `Color`  | The color of the line.                         |

```python
# Draw a line from the top-left to the bottom-right of the screen
graphics.stroke_line(canvas, 0, 0, 31, 31, consts.COLOR_WHITE)

# Draw a line from the top-right to the bottom-left of the screen
graphics.stroke_line(canvas, 31, 0, 0, 31, consts.COLOR_RED)

# Draw a line from the center of the screen to the bottom-right
graphics.stroke_line(canvas, 16, 16, 31, 31, consts.COLOR_GREEN)
```

The output of the following code is illustrated below:

![Line Example](./images/line_example.jpg)

### `stroke_rect(canvas, x1, y1, x2, y2, color)` <a name="stroke_rect"></a>

Draws the edges of a rectangle between the points (x1, y1) and (x2, y2) with the specified color.

| Argument | Datatype | Description                                            |
|----------|----------|--------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the rectangle on.                   |
| x1       | `int`    | The x-coordinate of one corner of the rectangle.       |
| y1       | `int`    | The y-coordinate of one corner of the rectangle.       |
| x2       | `int`    | The x-coordinate of the other corner of the rectangle. |
| y2       | `int`    | The y-coordinate of the other corner of the rectangle. |
| color    | `Color`  | The color of the rectangle.                            |

```python
# Draw a rectangle from (0,0) to (31,31) with a red border
graphics.stroke_rect(canvas, 0, 0, 31, 31, consts.COLOR_RED)

# Draw a rectangle from (5,5) to (25,25) with a green border
graphics.stroke_rect(canvas, 5, 5, 25, 25, consts.COLOR_GREEN)
```

The output of the following code is illustrated below:

![Rectangle Example](./images/rectangle_example_1.jpg)

### `fill_rect(canvas, x1, y1, x2, y2, color)` <a name="fill_rect"></a>

Draws and fills a rectangle between the points (x1, y1) and (x2, y2) with the specified color.

| Argument | Datatype | Description                                            |
|----------|----------|--------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the rectangle on.                   |
| x1       | `int`    | The x-coordinate of one corner of the rectangle.       |
| y1       | `int`    | The y-coordinate of one corner of the rectangle.       |
| x2       | `int`    | The x-coordinate of the other corner of the rectangle. |
| y2       | `int`    | The y-coordinate of the other corner of the rectangle. |
| color    | `Color`  | The color of the rectangle.                            |

```python
# Draw a rectangle from (0,0) to (31,31) with a red border
graphics.fill_rect(canvas, 0, 0, 31, 31, consts.COLOR_RED)

# Draw a rectangle from (5,5) to (25,25) with a green border
graphics.fill_rect(canvas, 5, 5, 25, 25, consts.COLOR_GREEN)
```

The output of the following code is illustrated below:

![Rectangle Example](./images/rectangle_example_2.jpg)

### `stroke_ellipse(canvas, cx, cy, rx, ry, color)` <a name="stroke_ellipse"></a>

Draws an ellipse centered at (cx, cy) with horizontal radius rx and vertical radius ry with the specified color.

| Argument | Datatype | Description                                    |
|----------|----------|------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the ellipse on.             |
| cx       | `int`    | The x-coordinate of the center of the ellipse  |
| cy       | `int`    | The y-coordinate of the center of the ellipse. |
| rx       | `int`    | The horizontal radius of the ellipse.          |
| ry       | `int`    | The vertical radius of the ellipse..           |
| color    | `Color`  | The color of the ellipse.                      |

```python
# Draw an ellipse centered at (16,16) with horizontal radius 10 and vertical radius 5
graphics.stroke_ellipse(canvas, 16, 16, 10, 5, consts.COLOR_WHITE)

# Draw an ellipse centered at (16,16) with horizontal radius 15 and vertical radius 15
graphics.stroke_ellipse(canvas, 16, 16, 15, 15, consts.COLOR_RED)
```

The output of the following code is illustrated below:

![Ellipse Example](./images/ellipse_example_1.jpg)

### `fill_ellipse(canvas, cx, cy, rx, ry, color)` <a name="fill_ellipse"></a>

Draws and fills an ellipse centered at (cx, cy) with horizontal radius rx and vertical radius ry with the specified color.

| Argument | Datatype | Description                                    |
|----------|----------|------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the ellipse on.             |
| cx       | `int`    | The x-coordinate of the center of the ellipse  |
| cy       | `int`    | The y-coordinate of the center of the ellipse. |
| rx       | `int`    | The horizontal radius of the ellipse.          |
| ry       | `int`    | The vertical radius of the ellipse..           |
| color    | `Color`  | The color of the ellipse.                      |

```python
# Draw an ellipse centered at (16,16) with horizontal radius 15 and vertical radius 15
graphics.fill_ellipse(canvas, 16, 16, 15, 15, consts.COLOR_RED)

# Draw an ellipse centered at (16,16) with horizontal radius 10 and vertical radius 5
graphics.fill_ellipse(canvas, 16, 16, 10, 5, consts.COLOR_WHITE)
```

The output of the following code is illustrated below:

![Ellipse Example](./images/ellipse_example_2.jpg)

### `stroke_circle(canvas, x, y, radius, color)` <a name="stroke_circle"></a>

Draws a circle of radius r at the point (x,y) with the specified color.

| Argument | Datatype | Description                                   |
|----------|----------|-----------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the circle on.             |
| x        | `int`    | The x-coordinate of the center of the circle  |
| y        | `int`    | The y-coordinate of the center of the circle. |
| radius   | `int`    | The radius of the circle.                     |
| color    | `Color`  | The color of the circle.                      |

```python
# Draw a circle centered at (16,16) with radius 15
graphics.stroke_circle(canvas, 16, 16, 15, consts.COLOR_RED)

# Draw a circle centered at (5,5) with radius 5
graphics.stroke_circle(canvas, 5, 5, 5, consts.COLOR_WHITE)
```

The output of the following code is illustrated below:

![Circle Example](./images/circle_example_1.jpg)

### `fill_circle(canvas, x, y, radius, color)` <a name="fill_circle"></a>

Draws and fills a circle of radius r at the point (x, y) with the specified color.

| Argument | Datatype | Description                                   |
|----------|----------|-----------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the circle on.             |
| x        | `int`    | The x-coordinate of the center of the circle  |
| y        | `int`    | The y-coordinate of the center of the circle. |
| radius   | `int`    | The radius of the circle.                     |
| color    | `Color`  | The color of the circle.                      |

```python
# Draw a circle centered at (16,16) with radius 15
graphics.fill_circle(canvas, 16, 16, 15, consts.COLOR_RED)

# Draw a circle centered at (5,5) with radius 5
graphics.fill_circle(canvas, 5, 5, 5, consts.COLOR_WHITE)
```

The output of the following code is illustrated below:

![Circle Example](./images/circle_example_2.jpg)

### `stroke_polyline(canvas, points, color)` <a name="stroke_polyline"></a>

Draws lines between all the points in a list with the specified color.

| Argument | Datatype | Description                                                                                                                |
|----------|----------|----------------------------------------------------------------------------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the polyline on.                                                                                        |
| points | `list[tuple[int,int]]` | The points the line is drawn between, expressed as a `list` of `tuples` containing the x- and y- coordinate of each point. |
| color | `Color` | The color to make the polyline.                                                                                            |

### `fill_polygon(canvas, points, color)` <a name="fill_polygon"></a>
| Argument | Datatype | Description                                                                                                                   |
|----------|----------|-------------------------------------------------------------------------------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the polygon on.                                                                                            |
| points | `list[tuple[int,int]]` | The points the polygon is drawn between, expressed as a `list` of `tuples` containing the x- and y- coordinate of each point. |
| color | `Color` | The color to make the polygon.                                                                                                |

### `draw_image(canvas, top_left_x, top_left_y, image)` <a name="draw_image"></a>

Draws the specified image with its top-left corner placed at (top_left_x, top_left_y).

| Argument | Datatype | Description                                                                                                                |
|----------|----------|----------------------------------------------------------------------------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the image on.                                                                                           |
| top_left_x | `int` | The x-coordinate of the top-left corner of the image on the canvas.                                                        |
| top_left_y | `int` | The y-coordinate of the top-left corner of the image on the canvas.                                                        |
| image | `numpy.ndarray` | The image to draw, expressed as a numpy `ndarray` with RGBA values for every pixel. See below for image-loading functions. |

```python
from PIL import Image
import numpy as np

# Load an image from a file
image = Image.open("bad_apple.png")

# Convert the image to a numpy array, and draw it on the canvas
graphics.draw_image(canvas, 0, 0, np.array(image))
```

The output of the following code is illustrated below, assuming the image is a 32x32 image:

![Image Example](./images/image_example.jpg)


### `draw_text(canvas, font, x, y, color, text)` <a name="draw_text"></a>

Draws text with the specified font with the (x, y) coordinate in the bottom left.

| Argument | Datatype | Description                                                    |
|----------|----------|----------------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the text on.                                |
| font     | `Font`   | The font size to draw the text with.                           |
| x        | `int`    | The x-coordinate of the bottom-left of the text on the canvas. |
| y        | `int`    | The y-coordinate of the bottom-left of the text on the canvas. |
| color    | `Color`  | The color to draw the text with.                               |
| text     | `str`    | The text to draw.                                              |

```python
# Draw the text "Hello!" at the top-left of the screen
graphics.draw_text(canvas, consts.FONT_4x6, 0, 6, consts.COLOR_WHITE, "Hello!")

# There's also FONT5x7 and FONT9x15 available
```

The output of the following code is illustrated below:

![Text Example](./images/text_example.jpg)

### `draw_centered_text(canvas, font, y, color, text)` <a name="draw_centered_text"></a>

Draws text horizontally centered on the screen at the specified y level.

| Argument | Datatype | Description                                               |
|----------|----------|-----------------------------------------------------------|
| canvas   | `Canvas` | The canvas to draw the text on.                           |
| font     | `Font`   | The font size to draw the text with.                      |
| y        | `int`    | The y-coordinate of the bottom of the text on the canvas. |
| color    | `Color`  | The color to draw the text with.                          |
| text     | `str`    | The text to draw.                                         |

```python
# Draw the text "Hello!" at the center of the screen
graphics.draw_centered_text(canvas, consts.FONT_4x6, 16, consts.COLOR_WHITE, "Hello!")
```

The output of the following code is illustrated below:

![Centered Text Example](./images/centered_text_example.jpg)
