from datetime import datetime
import os
import tempfile
from time import sleep
import zipfile
import shutil
import json
import platform
import subprocess
from pathlib import Path
from loguru import logger

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
        "disk": shutil.disk_usage(os.getcwd())._asdict(),
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

def screen_test():
    pass

def run_histograms():
    pass

def run_instrumentation():
    pass

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

def debug_main():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        patch_logger(tmpdir / "debug.log")

        z = zipfile.ZipFile("debug.zip", "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6)

        stats = gather_stats()
        z.writestr("README.md", README)
        z.writestr("stats.json", json.dumps(stats, indent=2))

        screen_test()

        run_histograms()

        run_instrumentation()

        compile_results()

        z.write(tmpdir / "debug.log", "debug.log")

        z.close()
