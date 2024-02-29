# Internals

This document is a guide to the inner workings and mechanisms of this sign.

## Table of Contents

- [Internals](#internals)
  - [Table of Contents](#table-of-contents)
  - [Lifecycle Of A Screen Task](#lifecycle-of-a-screen-task)
    - [Initialization](#initialization)
    - [Preparation](#preparation)
    - [Execution](#execution)
      - [LCD Screen](#lcd-screen)
    - [Cleanup](#cleanup)
  - [Lifecycle Of This Program](#lifecycle-of-this-program)

## Lifecycle Of A Screen Task

The lifecycle of a screen task can be broken down into the following stages:

1. **Initialization**: The task is created and initialized.
2. **Preparation**: The task is prepared for execution.
3. **Execution**: The task is executed.
4. **Cleanup**: The task is cleaned up and destroyed.

Each of these stages is described in detail below.

### Initialization

The initialization stage is the first stage, and its sole purpose is to create the task within the system, by calling `__init__`. This stage is ran only once, and is ran while the screen is still being created. This stage may be called well in advance of any other task, and may be the only stage that is called in some cases.

Typically, no action is needed to be taken during this stage. However, if the task requires any heavy proessing before hand, like downloading a video and preparing it for playback, this is the stage to do it in. (See `bad_apple.py` for an example of this.)

### Preparation

The preparation stage is the second stage, and its purpose is to prepare the task for execution. This stage will be called right before any frames are rendered, and is a good chance to initialize any resources that will be used during the task's execution.

For instance, fetching the latest data from an API is a good thing to do during this stage, as in `weather.py`.

Returning `True` from this stage will signal that the task is ready to be executed. Returning `False` will signal that the task *cannot* be executed, and will be skipped. This is useful for tasks that rely on external resources being present, like a network connection.

```python
def prepare(self) -> bool:
    if not internet_is_available():
        return False # there's no internet! skip this task!
    self.weather_data = fetch_weather_data()
    return True # we're ready to go!
```

### Execution

The execution stage is the third stage, and its purpose is to actually execute the task. This stage will be called once per frame, and is a good chance to update the task's state, and render the task's output.

Two parameters are passed to the `draw_frame` method: `canvas` and `delta_t`. `canvas` is an instance of the `Canvas` class, and is used to draw the task's output. `delta_t` is the time since the last frame.

Note: The canvas is cleared before `draw_frame` is called!

```python
def draw_frame(self, canvas: Canvas, delta_t: timedelta) -> Optional[bool]:
    graphics.draw_text(canvas, self.weather_data['temperature'])
    # ...
```

Returning `True` from this stage will signal that the task is done, and can be ended sooner. Returning `False` will signal that the task is not done, and will most likely be called again. Returning nothing is the same as returning `False`.

#### LCD Screen

Special to the C4 sign, there is a special `get_lcd_text` method that is called alongside `draw_frame`. This method is used to render the task's output to the LCD screen, and is called every so often. This method is optional, and, if not present, will output a default message.

This should return a string that is 32 characters long, and will be displayed on the LCD screen (16 characters per line, 2 lines).

```python
def get_lcd_text(self) -> str:
    return "The weather is nice today!".ljust(32) # pad the string to 32 characters
```

### Cleanup

The cleanup stage is the final stage, and its purpose is to clean up any resources that were used during the task's execution. This stage will be called after the task is done, and is a good chance to free any resources that were allocated during the task's execution.

The `forced` parameter is called with `True` if the task is being forced to end (like being overriden, or running out of time), and `False` if the task is ending naturally (returning `True` from `draw_frame`). This is useful for tasks that need to clean up resources in a specific way.

```python
def teardown(self, forced: bool = False):
    self.weather_data = None
```

## Lifecycle Of This Program

TODO: Write this :3!
