from datetime import datetime, timedelta
import math
import os
import tempfile
from time import sleep, perf_counter
import zipfile
import shutil
import json
import platform
import subprocess
import statistics
from pathlib import Path
from loguru import logger

from c4_sign.lib.canvas import Canvas
from c4_sign.screen import Screen

try:
    from pyinstrument import Profiler
    from pyinstrument.renderers import SpeedscopeRenderer
    from matplotlib import pyplot as plt
except ImportError:
    print("Missing dependencies for debug mode!")
    print("  try pip install -e .[misc]")
    exit(1)

try:
    from rich.progress import track
except ImportError:
    def track(iter, description=""):
        yield from iter

def patch_logger(logfile):
    logger.add(logfile, level="DEBUG")

def gather_stats():
    data = {
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "memory": os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'),
        "disk": shutil.disk_usage(Path.cwd())._asdict(),
        "system": platform.uname()._asdict(),
        "git": {
            "branch": subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip(),
            "commit": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "started": datetime.now().isoformat(),
    }
    return data

def screen_test(screen: Screen):
    pass

def run_histograms(screen: Screen, zip_file: zipfile.ZipFile, draw_to_screen: bool):
    # this currently doesn't work quite right on anything that's truly random
    # currently, that's SortingAlgos.
    # (stuff like pong isn't affected, because that only uses randomness for the inital state, not changing the implemetaion like SortingAlgos)
    
    # this also, fundamentally, DOES NOT WORK on any external tasks (those written in Java, for example)
    # so, uh, it'll still work, but it'll produce garbage data.
    canvas = Canvas()
    tasks = screen.screen_manager.current_tasks
    delta_t = timedelta(seconds=1 / 24)
    s = screen.screen

    for task in track(tasks, "Histograms"):
        task.capture_histogram = True

        task.prepare()
        frames = 0
        start = perf_counter()
        while True:
            canvas.clear()
            text = task.get_lcd_text()
            result = task.draw(canvas, delta_t)
            frames += 1
            if draw_to_screen:
                s.update_lcd(text)
                s.update_display(canvas)
            if result:
                break
        end = perf_counter()
        elapsed = end - start

        task.capture_histogram = False

        # do the whole... plot thing
        plt.style.use("ggplot")
        plt.suptitle(f"Draw time frequency for {task.title} by {task.artist}", wrap=True)
        plt.title(f"(n = {len(task.draw_time_samples)} frames)", fontsize="medium", wrap=True)
        plt.xlabel("Draw Times (ms)")
        plt.ylabel("Frames")

        acceptable = 41.66
        max_time = max(max(task.draw_time_samples), acceptable)
        bin_width = 2.5 # milliseconds

        if len(task.draw_time_samples) > 0:
            median = statistics.median(task.draw_time_samples)
            plt.axvline(median, color="black", label="Median Draw Time", linewidth=2)
        
        plt.axvline(acceptable, color="red", label="Maximum Acceptable Draw Time", linewidth=2)
        plt.legend(loc="best")
        plt.hist(task.draw_time_samples, bins=math.ceil(max_time/bin_width), range=(0, max_time), edgecolor="white")

        plt.tight_layout()

        with zip_file.open(f"histograms/plots/{task.title}_histogram.png", "w") as f:
            plt.savefig(f, format="png")
        plt.close()

        zip_file.writestr(f"histograms/raw/{task.title}_raw.json", json.dumps(task.draw_time_samples, indent=2))

        zip_file.writestr(f"histograms/info/{task.title}_info.json", json.dumps({
            "title": task.title,
            "artist": task.artist,
            "frames": frames,
            "samples": len(task.draw_time_samples),
            "max_time": max_time,
            "median": median,
            "avg_fps": len(task.draw_time_samples) / elapsed,
        }, indent=2))

        # yippie



def run_instrumentation(screen: Screen, zip_file: zipfile.ZipFile, draw_to_screen: bool):
    canvas = Canvas()
    tasks = screen.screen_manager.current_tasks
    delta_t = timedelta(seconds=1 / 24)
    s = screen.screen

    for task in track(tasks, "Profiling"):
        task.prepare()
        frames = 0
        start = perf_counter()
        with Profiler() as profiler:
            while True:
                canvas.clear()
                text = task.get_lcd_text()
                result = task.draw(canvas, delta_t)
                frames += 1
                if draw_to_screen:
                    s.update_lcd(text)
                    s.update_display(canvas)
                if result:
                    break
        end = perf_counter()
        elapsed = end - start

        profile_out = profiler.output(renderer=SpeedscopeRenderer(show_all=True))

        zip_file.writestr(f"instrumentation/{task.title}_profile.json", profile_out)
        
        zip_file.writestr(f"instrumentation/{task.title}_info.json", json.dumps({
                "title": task.title,
                "artist": task.artist,
                "frames": frames,
                "elapsed": elapsed,
                "fps": frames / elapsed,
            }, indent=2))
        
def compile_results():
    pass

README = """\
# C4 Sign Debug Mode

Hello! This ZIP file contains a bunch of debug information about the execution of the C4 Sign.

## What's Included

- `README.md` - This file.
- `stats.json` - System information and other metadata.
- `debug.log` - The log file.

Good luck, and have fun! <3
"""

def debug_main(draw_to_screen: bool = True, instrumentation: bool = False):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        patch_logger(tmpdir / "debug.log")

        z = zipfile.ZipFile("debug.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6)

        stats = gather_stats()
        z.writestr("README.md", README)
        z.writestr("stats.json", json.dumps(stats, indent=2))

        s = Screen()

        if draw_to_screen:
            # why would we wanna do the screen test if we're not drawing to the screen?
            s.init_matrix(simulator=True, update_tasks=False)

            screen_test(s)
        s.screen_manager.update_tasks()

        run_histograms(s, z, draw_to_screen)

        if instrumentation:
            run_instrumentation(s, z, draw_to_screen)

        compile_results()

        z.write(tmpdir / "debug.log", "debug.log")

        z.close()
