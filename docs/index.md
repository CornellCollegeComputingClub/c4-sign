# LED Sign Documentation

The following is a list of topics you might need to know in order to write your own sign program.

# Existing Screen Tasks

A list of .webp simulations of existing screen tasks can be found [here](./screen_tasks.md).

# Screen Tasks & Tutorial
Each program the screen displays is a [Screen Task](./internals.md).
They contain the code needed to draw pictures on the display, as well as any setup or cleanup that needs to take place.  
  
You can write screen tasks in either Python or Java. Ultimately, you can choose whichever you are more familiar with, but here are some reasons you might want to choose each one. A lot of people have more familiarity with Python at Cornell, but the Python interpreter is much slower than Java and the graphics functions are much less advanced. Even simple Python tasks that just change the color of most of the pixels on the screen can take long enough that the sign can't run at 24 FPS. However, things like loading images and drawing them to the screen can be very fast.
Java tasks are much faster and it is much easier to stay within the time limit to achieve a 24 FPS framerate. Additionally, within a Java Task, you can use graphics functionality from Java's Advanced Web Types class, which you can use to draw shapes, lines, circles, text, and much more. If drawing each frame of your animation is a complicated procedure, it might be best to be a Java task. However, if the animation is the same each time the task runs, you can take advantage of a prerendering feature that will help run them at 24 FPS in Python.

To see the difference between Python and Java tasks, have a look at [RainbowWave](../c4_sign/screen_tasks/rainbow_wave.py) and [RainbowWaveJava](../c4_sign/java_c4sign/src/main/java/com/cornellcollegecomputingclub/c4sign_tasks/RainbowWaveJava.java).

See the [Internals](./internals.md) page to learn about their structure.


For a guide on writing your own Python screen task, see the [Tutorial page](./tutorial.md)!

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