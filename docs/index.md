# LED Sign Documentation

The following is a list of topics you might need to know in order to write your own sign program.

# Existing Screen Tasks

A list of .gif recordings simulations of existing screen tasks can be found [here](./screen_tasks.md).

# Tutorial / Screen Task Internals
Each program the screen displays is a [Screen Task](./internals.md).
They contain the code needed to draw pictures on the display, as well as any setup or cleanup that needs to take place.
See the [Internals](./internals.md) page to learn about their structure.
For a guide on writing your own screen task, see the [Tutorial page](./tutorial.md)!

# Graphics Library
The sign has many graphics functions that can help you draw images on the screen.
For example, it has helper methods for drawing squares, circles, ellipses, lines, and many other shapes on the screen.
You may also want to draw text or pictures (Like PNGs) to the screen.
To learn how to use the graphics library functions, see the [Graphics Library page](./graphics-library.md).

# Loading External Assets
You may want access to external assets within your program.
For example, you may want to download an image or the frames of a YouTube video.
This is an expensive operation that shouldn't be done while the sign is actively running, so we have written functions to cache the results of operations like these.
To learn more about using external media or downloaded files, see the [Assets page](./assets.md).

# Installed Libraries and other helpful resources
The sign has many libraries already installed.
It also has its own custom library of useful functions, that might not be directly related to graphics.
You can view them [here](./resources.md).
These include things such as the Message of the Day text, nice looking colors, the available fonts, and much more.