# How To Make a Program for the Sign

Hello! This guide will guide you in making your very own program for C4's sign! This guide only covers the basics, but we will briefly mention some more advanced topics.

## Setting Up Your Environment

In order to work on the sign, you will first need to have Python 3.9 (or above) and git installed. Additionally, you will need a GitHub account so you can add your work later, and we recommend using VS Code to work on your code.

With the necessities out of the way, let's set up your environment!

First, you must fork the repository on GitHub. This will create a copy of the repository under your own GitHub account. To do this, just hit the `Fork` button in the top right corner, and follow the instructions.

Next, we must clone the repository to your computer. You may use a GUI if you have one, but we'll be using the command line for this guide.

```sh
luna (~) > cd Documents/Code
luna (~/Documents/Code) > git clone https://github.com/itsactuallyluna9/c4-sign.git
Cloning into 'c4-sign'...
remote: Enumerating objects: 606, done.
remote: Counting objects: 100% (311/311), done.
remote: Compressing objects: 100% (196/196), done.
remote: Total 606 (delta 191), reused 214 (delta 103), pack-reused 295
Receiving objects: 100% (606/606), 241.68 KiB | 1.55 MiB/s, done.
Resolving deltas: 100% (355/355), done.
luna (~/Documents/Code) > cd c4-sign
luna (c4-sign) > # we have our code!
```

We now have the code on our computer! We still have a bit of work to do, like installing all of our dependencies to run the simulator. This is easily accomplished by running the following command in the `c4-sign` directory we just downloaded:

```sh
$ pip install -e '.[simulator]'
```

(Note: we'll be using the `$` character to indicate a shell command from here on out!)

Once that finishes, we're good to go!

## Hello, World!

We're going to write a simple "Hello, World!" program that will fill the screen with our favorite color!

First, we must make a new "screen task", which is just a sub-program that the main program runs. All of these sub-programs live in `c4_sign/screen_tasks`.

To create a new screen task, either copy `demo_task.py` and rename that file, or, if you're feeling adventurous, start a new file!

We'll be copying and using `demo_task.py` as an example, and making a file called `favorite_color.py`. Open it up, and you'll be met with this:

```py
from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics


class Demo(ScreenTask):
    title = "Demo"
    artist = "Mac Coleman"
    ignore = True

    def prepare(self):
        self.frame = 0
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        r, g, b = self.frame, 0, 255 - self.frame
        graphics.fill_screen(canvas, (r, g, b))
        self.frame = (self.frame + 4) % 255

        if self.elapsed_time > self.suggested_run_time:
            return True
        else:
            return False
```

Starting at the top, we import a class called ScreenTask and our graphics library, and make our class (currently called Demo) a subclass of ScreenTask. It's not important to know *what* ScreenTask does right now, other than it allows the main program to recognize that this is a sub-program.

Next up, we have the `title` and `artist` variables. Change these to the title of your program and your name! (While you're at it, rename the class also!)

Also, remember to remove the `ignore` variable! (If `ignore` is true, the sign will outright ignore your sub-program's existence!)

```diff
- class Demo(ScreenTask):
-     title = "Demo"
-     artist = "Mac Coleman"
-     ignore = True
+ class FavoriteColor(ScreenTask):
+     title = "Favorite Color"
+     artist = "Luna"
```

Continuing onward, we have the `prepare(self)` function. Before your program gets ran, this function gets called, allowing you to set up anything that you need to set up. For now, though, we'll keep it as-is.

Now we get to `draw_frame(...)`. This function is called *every frame*, and is where you actually draw to the screen. You get a `Canvas` object, which is a 32x32 grid, and a `delta_time` object, which is the time between the last frame and the current frame.

We'll replace the code within `draw_frame(...)` with the following:

```py
def draw_frame(self, canvas, delta_time):
	graphics.fill_screen(canvas, 0xd883ff)
```

All we're doing here is filling the canvas, with help from our graphics library, with a color. In this case, we're using a shade of purple! (If you're curious, it's from the flower heliotrope!)

Now, all we need to do now is test it out!

## Running the Simulator

Running the simulator is quite simple, we just need to run:

```sh
$ python3 -m c4_sign --simulator
```

Which will open up your web browser with a simulation of the physical display! Once the sign gets to our program, we'll see the screen turn a lovely shade of purple.

> [!TIP]
> Impatient? Select the class name from the dropdown at the bottom and hit `send`! It'll immediately start your program!

...hm. It's pretty, but... it's quite lacking. Although I love this shade of purple, staring at it for 60 seconds is not ideal.

We'll press Ctrl+C in our terminal to stop the simulator, and do some more work on it.

## Adding Motion

We're going to keep it simple, and have a ball of our perferred color fly around the screen for a bit!

We'll want to add some variables to keep track of where our ball is, and where it's heading. To do this, we'll add some variables to our `prepare(self)` function (making sure to `import random`)...

```py
def prepare(self):
    # position
    self.x = random.randint(0, 31)
    self.y = random.randint(0, 31)
    
    # momentum
    self.dx = random.choice([-1, 1])
    self.dy = random.choice([-1, 1])
    
    # constants
    self.color = 0xd883ff
    self.radius = 3
    return super().prepare()
```

We'll also need to modify our `draw_frame(...)` function to move and draw the ball!

```py
def draw_frame(self, canvas, delta_time):
    # 
    self.x += self.dx
    self.y += self.dy

    # check for collisions
    if self.x < (0 + self.radius) or self.x > (31 - self.radius):
        self.dx = -self.dx
    if self.y < (0 + self.radius) or self.y > (31 - self.radius):
        self.dy = -self.dy
    
    # draw the ball
    graphics.fill_circle(canvas, self.x, self.y, self.radius, self.color)
```

## Re-Running the Simulator

Re-running the simulator, we see now that our ball flies around the screen! Take a moment and admire its beauty.

> [!NOTE]
> We're not going to fix it here, but the ball can sometimes spawn in a wall. Sorry!

## Publishing Our Work

Now that you have your beautiful creation, how *exactly* do we get it on the sign? Simple, we must submit a **Pull Request**!

To get started, we need to *commit* our work to the repository that you cloned at the start of this tutorial.

```sh
$ git add c4_sign/screen_tasks/picasso_hates_us.py
$ git commit -m "my super cool creation"
$ git push
```

> [!TIP]
> You can use anything you feel comfortable with to commit and push! VS Code has a `Source Control` panel you can use to do the same thing, or you can use something like `lazygit`, `Fork`, or `Github Desktop`.

Once you've done that, you'll need to open up a **Pull Request**. For futher details, see [GitHub's documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)!

Now, all that's left to do is wait. One of us will come and review your awesome program, give you feedback if neccessary, and merge your code in! Once that happens, check the sign in a day or so and *presto*!

## Further Reading
