# C4 Sign
funny sign go brrrrrrrr

![An image of the C4 Sign, displaying the C4 Logo](./docs/images/demo.jpg)

The C4 Sign is an LED sign that students can write programs for to display at our events on campus!
It features a 32x32 color LED display for graphics and a 16x2 character LCD screen for text.

If you are interested in writing a display program for it, please make a fork of this repository.
Get in touch with us if you have any questions or want advice for how to write your program!

The LED Sign channel of our discord server is a great place to get advice both from club executives and from other students.
Feel free to make whatever you like for the sign, this is a chance to use your programming skills to channel your creativity and self-expression!

# Installation and Setup

Check [the tutorial](./docs/tutorial.md) to learn how you can begin writing your own sign programs.

# Program Examples
You can see simulated outputs of the display programs [here](./docs/screen_tasks.md).
If you want to see how each task works, the programs can be found in `/c4_sign/screen_tasks`.

## Documentation
Our documentation is currently incomplete, but much of the screen's workings can be found in the `/docs/` directory.
See the [documentation home page](./docs/index.md).

## Simulator

The simulator is a simple program that simulates the sign. It's not perfect, but it's good enough for testing.
It allows you to write programs for the sign without physical access!

```bash
python3 -m pip install -e '.[simulator]'
python3 -m c4_sign --simulator
```

You can test the simulator at any time you like by running with the following command:
```bash
python3 -m c4_sign --simulator
```
This will open a new browser window where you can interact with the sign simulator. Currently, it looks like this:
![The simulator displaying the "pong" task](./docs/images/simulator.png)

It shows you a visualization of the 32 by 32 pixel matrix, and the attached 16x2 character LCD screen.
You can use the dropdown menu at the bottom to choose a task to run, then press 'send' to run it.

You can use the simulator to test out your program without needing to be near the sign all the time!
Whenever you make changes to your program, visualizing them is as simple as running the above command and selecting it in the simulator

## Real Sign

[To be written]

```bash
python3 -m pip install -e '.[physical]'
python3 -m c4_sign
```

# Wishlist
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

## Updates

Updates happen either:
- Every 24 hours (shortly after midnight)
- When the script is first launched (after like a reboot)