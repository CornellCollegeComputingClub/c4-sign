import argparse

from c4_sign.screen import init_matrix, update_screen
from c4_sign.ScreenManager import ScreenManager
from c4_sign.tasks import TaskManager


def run_gif():
    from datetime import timedelta

    from PIL import Image, ImageDraw, ImageFont

    from c4_sign.lib.canvas import Canvas

    screen_manager = ScreenManager()
    screen_manager.update_tasks()
    delta_t = timedelta(seconds=1 / 24)
    canvas = Canvas()
    tasks = screen_manager.current_tasks
    font = ImageFont.truetype("Arial", 16)
    for task in tasks:
        print(f"Running {task.__class__.__name__}")
        images = []
        task.prepare()
        while True:
            canvas.clear()
            text = task.get_lcd_text()
            result = task.draw(canvas, delta_t)
            img = Image.new("RGB", (256, 384))
            draw = ImageDraw.Draw(img)
            for y in range(32):
                for x in range(32):
                    r, g, b = canvas.get_pixel(x, y)
                    draw.rectangle((x * 8, y * 8, (x + 1) * 8, (y + 1) * 8), fill=(r, g, b))
            # add text
            draw.text((0, 320), text[16:], font=font, fill=(255, 255, 255))
            draw.text((0, 300), text[:16], font=font, fill=(255, 255, 255))
            images.append(img)
            if result:
                break
        images[0].save(
            f"gif/{task.__class__.__name__}.gif",
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
        )

    exit(0)


def main(args=None):
    if args.gif:
        print("GIF mode!")
        return run_gif()
    init_matrix(args.simulator)
    tm = TaskManager()

    print("Finishing up startup...")

    while True:
        tm.check_and_run_tasks()
        update_screen()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", action="store_true")
    parser.add_argument("--gif", action="store_true")
    parser.add_argument("--profile", action="store_true")
    args = parser.parse_args()
    if args.profile:
        try:
            from pyinstrument import Profiler
            from pyinstrument.renderers import SpeedscopeRenderer
        except ImportError:
            print("Please install pyinstrument to use the --profile flag")
            print("try pip install -e .[misc]")
            exit(1)

        with Profiler() as profiler:
            try:
                main(args)
            except BaseException:
                pass
        print("Writing profile to /tmp/profile.speedscope.json")
        with open("/tmp/profile.speedscope.json", "w") as f:
            f.write(profiler.output(renderer=SpeedscopeRenderer(show_all=True)))
    else:
        main(args)
