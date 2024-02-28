# C4 Canvas Graphics API
This guide explains each of the functions in the graphics API that you can use to write your display programs.
If you are looking to learn how to write a basic display program, see the tutorial. INSERT LINK HERE.

Each display program must produce "frames" for the screen to display.
These frames are represented by `Canvas` objects that abstract the operations done on the screen.
This guide will go into detail on each of the operations available for `Canvas` objects to draw your display.

# Table of Contents

1. Datatypes
   1. [Canvas](#Canvas)
      1. set_pixel
   1. [Color](#Color)

   3. Font
2. Graphics Library
   1. fill_screen
   2. clear_screen
   3. stroke_line
   4. stroke_rect
   5. fill_rect
   6. stroke_ellipse
   7. fill_ellipse
   8. stroke_circle
   9. fill_circle
   10. stroke_polyline
   11. fill_polygon
   12. draw_image
   13. draw_text

## Datatypes


### Canvas <a name="Canvas"></a>
The `Canvas` class is what you use to draw images on the LED screen!

TODO: Fill this out

### Color <a name="Colors"></a>
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
solid_white = 0xffffff00
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
TODO: ADD IMAGE HERE
