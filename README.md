# C4 Sign
funny sign go brrrrrrrr

![An image of the C4 Sign, displaying the C4 Logo](./docs/images/demo.png)

The C4 Sign is an LED sign that students can write programs for to display at our events on campus!
Programs can be written in either Java or Python.
It features a 32x32 color LED display for graphics and a 16x2 character LCD screen for text.

If you are interested in writing a display program for it, please make a fork of this repository.
Get in touch with us if you have any questions or want advice for how to write your program!

The LED Sign channel of our discord server is a great place to get advice both from club executives and from other students.
Feel free to make whatever you like for the sign, this is a chance to use your programming skills to channel your creativity and self-expression!

## Tutorial

Check [the tutorial](./docs/tutorial.md) to learn how you can begin writing your own sign programs.

## Program Examples
You can watch each display program [here](./docs/screen_tasks.md).
If you want to see how each task works, the programs can be found in `/c4_sign/screen_tasks` and `/c4_sign/java_c4sign/src/main/java/com/cornellcollegecomputingclub/c4sign_tasks`.

## Documentation
Our documentation is currently incomplete, but much of the screen's workings can be found in the `/docs/` directory.
See the [documentation home page](./docs/index.md).

## Simulator

The simulator is a simple program that simulates the sign.
It allows you to write programs for the sign without physical access!

![The simulator displaying the "pong" task](./docs/images/simulator.png)

It shows you a visualization of the 32 by 32 pixel matrix, and the attached 16x2 character LCD screen.
You can use the dropdown menu at the bottom to choose a task to run, then press 'send' to run it.

You can use the simulator to test out your program without needing to be near the sign all the time!
Whenever you make changes to your program, visualizing them is as simple as running the above command and selecting it in the simulator

## Wishlist
The following is a list of programs that could be neat to have on our sign!
If you are unsure what to make, you can use the list below as inspiration.

* [A digital 'rain' effect, like from The Matrix](https://www.youtube.com/watch?v=MUVo20q6tx8)
* [Something like boids!](https://www.youtube.com/watch?v=bqtqltqcQhw)
* [Something like the bouncing DVD logo!](https://www.youtube.com/watch?v=QOtuX0jL85Y)
* [Something like Conway's game of life!](https://www.youtube.com/watch?v=C2vgICfQawE)
* Simulating a classic video game, like [Spacewar](https://www.youtube.com/watch?v=1EWQYAfuMYw&t=729), [Tetris](https://www.youtube.com/watch?v=O0gAgQQHFcQ), [Breakout](https://www.youtube.com/watch?v=NOGO49j5gCE), or [Pong](https://www.youtube.com/watch?v=fiShX2pTz9A)
* Simulated fireworks!
* Something that displays the Message of the Day! (Found in `/c4_sign/consts.py`)
* Something to celebrate the season or something you like!

If you want to make something, but are struggling with ideas, feel free to reach out to us or ask in our Discord.

# Installation

In order to make a program that runs on the sign, you will have to locally install the sign software and simulator so that you can test your program.

Here's how you can install the C4 Sign software:

1. Make sure you have Python and Git installed. Python 3.9 or above should be good. *If you want to write your program with Java, which is recommended for graphics-intense tasks, make sure to also install Maven.*
2. Sign into Github and make a fork of this repository.
3. Navigate to the folder where you would like to download the software, and clone your fork of our git repository!
`git clone https://github.com/{Your username here}/c4-sign`
4. Enter the `c4-sign` repository by typing `cd c4-sign`.
5. **Optional:** If you want to, you can create a virtual environment for this project. If you don't know what a virtual environment is, you can skip this step. If you want to make one, run `python3 -m venv ./venv` and then activate the virtual environment in whichever way you typically do that with your operating system.
6. Run `python3 -m pip install -e '.[simulator]'`. This will install the simulator software on your computer.

Congrats! You can now run the simulator in **python-only** mode. To do so, run:
`python3 -m c4_sign --simulator --disable-java` and a new web browser window will appear with the simulator! It may take a while for that to happen as it will download certain resources first.

If you want to work with Java, there are a few more steps.  
  
7. Run `python3 tools/setup_java_project.py`. This will make sure the necessary Java and Python dependencies are available.  
8. Run `python3 tools/compile_java_project.py`. This will compile the Java project correctly for the sign software to use it. **You must run this command every time you want to test changes to a Java file.**

Nice! Now you can run the simulator in **python and java mode**. To do so, run:
`python3 -m c4_sign --simulator`. The Java and the Python tasks should now be available!

Problems?

Please email us or ask for help in the `#led-sign` channel of our discord server!

## Updates

Updates happen either:
- Every 24 hours (shortly after midnight)
- When the script is first launched (after like a reboot)