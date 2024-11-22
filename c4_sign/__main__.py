import argparse

from c4_sign.screen import init_matrix, update_screen
from c4_sign.ScreenManager import ScreenManager
from c4_sign.log import setup_logger
from c4_sign.tasks import TaskManager
from loguru import logger
import sys


def run_gif():
    from datetime import timedelta
    from pathlib import Path

    from PIL import Image, ImageDraw, ImageFont

    from c4_sign.lib.canvas import Canvas

    try:
        from rich.progress import track
    except ImportError:

        def track(iter, description=""):
            yield from iter

    screen_manager = ScreenManager(False, True)
    screen_manager.update_tasks()
    delta_t = timedelta(seconds=1 / 24)
    canvas = Canvas()
    tasks = screen_manager.current_tasks
    font = ImageFont.truetype("Courier", 16)
    with open("docs/screen_tasks.md", "w") as f:
        f.write("# Screen Tasks\n\n")
        for task in sorted(tasks, key=lambda x: x.__class__.__name__):
            f.write(f"## {task.__class__.__name__}\n")
            f.write(f"**Title**: {task.title}\n\n")
            f.write(f"**Artist**: {task.artist}\n\n")
            if task.__doc__:
                f.write(f"Description:\n```python\n{task.__doc__}\n```\n")
            f.write(f"![{task.__class__.__name__}](images/screen_tasks/{task.__class__.__name__}.webp)\n")
    source = Path("docs/images/screen_tasks")
    source.mkdir(parents=True, exist_ok=True)
    existing = [x.stem for x in source.glob("*.webp")]
    removed = [x for x in existing if x not in [task.__class__.__name__ for task in tasks]]
    for remove in removed:
        print(f"Removing {remove}.webp")
        (source / f"{remove}.webp").unlink()
    tasks = [task for task in tasks if task.__class__.__name__ not in existing]
    for task in track(tasks, description="Converting!"):
        print(f"Running {task.__class__.__name__}")
        duration = 0
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
            duration += 1 / 24
            if result or duration > 30:
                break
        images[0].save(
            source / f"{task.__class__.__name__}.webp",
            save_all=True,
            append_images=images[1:],
            duration=(1 / 24) * 1000,
            loop=0,
        )

    exit(0)

def generate_pr_preview():
    from datetime import timedelta
    from pathlib import Path

    from PIL import Image, ImageDraw, ImageFont

    from c4_sign.lib.canvas import Canvas
    from subprocess import run
    import importlib
    from c4_sign.base_task import ScreenTask, OptimScreenTask

    try:
        from rich.progress import track
    except ImportError:

        def track(iter, description=""):
            yield from iter

    logger.info("Generating PR preview!")
    delta_t = timedelta(seconds=1 / 24)
    canvas = Canvas()
    font = ImageFont.truetype("./Source_Code_Pro/source-code-pro-v23-latin-regular.ttf", 16)
    source = Path("preview")
    source.mkdir(parents=True, exist_ok=True)
    # git diff --name-only -r HEAD^1 HEAD
    changed_files = run(["git", "diff", "--name-only", "-r", "HEAD^1", "HEAD"], capture_output=True, text=True).stdout.splitlines()
    # anything in c4_sign/screen_tasks/*.py we wanna generate
    tasks = []
    for file in changed_files:
        if "c4_sign/screen_tasks" in file:
            logger.debug("Found changed file: {}", file)
            # we need to import the module
            obj = importlib.import_module(file.replace("/", ".")[:-3])
            for name, obj in obj.__dict__.items():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, ScreenTask)
                    and obj not in (ScreenTask, OptimScreenTask)
                    and obj.ignore is False
                ):
                    if issubclass(obj, OptimScreenTask):
                        obj.should_optimize = False
                    tasks.append(obj())
    for task in track(tasks, description="Converting!"):
        logger.info("Running {}", task.__class__.__name__)
        print(f"Running {task.__class__.__name__}")
        duration = 0
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
            duration += 1 / 24
            if result or duration > 30:
                break
        logger.info("Saving {}", task.__class__.__name__)
        images[0].save(
            source / f"{task.__class__.__name__}.webp",
            save_all=True,
            append_images=images[1:],
            duration=(1 / 24) * 1000,
            loop=0,
        )
    logger.info("Processed all PR preview tasks")

    exit(0)

def upload_histograms(args):
        import subprocess
        import tempfile
        from pathlib import Path
        import arrow
        import requests

        directory = "c4_histograms"
        tarball = "c4_histograms.tar.gz"
        temp_path = tempfile.gettempdir()

        print(f"Histograms available at {Path(temp_path) / directory}")

        if args.no_upload:
            print("Skipping histogram upload")
            return

        proc = subprocess.run(["tar", "-C", temp_path, "-czf", f"{Path(temp_path) / tarball}", directory])
        if proc.returncode != 0:
            print(f"Failed to tar histograms directory at {Path(temp_path) / directory}")
            print(proc.stderr.decode() if proc.stderr is not None else "")
            print("Unable to compress histograms!")
            print("Unable to upload histograms!")
            return

        files = {
            'reqtype': (None, 'fileupload'),
            'time': (None, '1h'),
            'fileToUpload': open(Path(temp_path) / tarball, 'rb'),
        }

        response = requests.post('https://litterbox.catbox.moe/resources/internals/api.php', files=files)

        if response.ok:
            print("Successfully uploaded histograms!")
            print(f"Histograms can be found at: {response.text} as a .tar.gz file.")
        else:
            print("Failed to upload histograms: " + str(response))

@logger.catch
def main(args=None):
    setup_logger()
    logger.info("Starting up!")
    if args.purge_cache:
        from c4_sign.lib.assets import purge_cache

        purge_cache()
        print("Cache purged!")
    if args.generate_pr_preview:
        return generate_pr_preview()
    if args.gif:
        logger.info("Starting in GIF mode")
        print("GIF mode!")
        if args.purge_cache:
            # we're also gonna clear the gif folder, just so we're forced to regenerate them
            from pathlib import Path
            from shutil import rmtree

            logger.info("Purging GIF folder")
            source = Path("docs/images/screen_tasks")
            rmtree(source, ignore_errors=True)
            logger.info("GIF folder purged!")
        return run_gif()
    init_matrix(args.simulator, args.histograms, not args.disable_java)
    tm = TaskManager()

    logger.info("Finishing startup; starting main loop!")

    while True:
        tm.check_and_run_tasks()
        update_screen()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", action="store_true")
    parser.add_argument("--disable-java", action="store_true")
    parser.add_argument("--gif", action="store_true")
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--histograms", action="store_true")
    parser.add_argument("--no-upload", action="store_true")
    parser.add_argument("--purge-cache", action="store_true")
    parser.add_argument("--generate-pr-preview", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.profile:
        try:
            from pyinstrument import Profiler
            from pyinstrument.renderers import SpeedscopeRenderer
        except ImportError:
            print("Please install pyinstrument to use the --profile flag")
            print("try pip install -e .[misc]")
            exit(1)

        with Profiler(interval=0.01) as profiler:
            try:
                main(args)
            except BaseException:
                pass
        print("Writing profile to /tmp/c4_profile/profile.speedscope.json")
        with open("/tmp/c4_profile/profile.speedscope.json", "w") as f:
            f.write(profiler.output(renderer=SpeedscopeRenderer(show_all=True)))

    elif args.histograms:
        try:
            main(args)
        except KeyboardInterrupt:
            pass

        upload_histograms(args)

    else:
        main(args)
