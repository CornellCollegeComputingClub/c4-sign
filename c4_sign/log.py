import platform
from loguru import logger
import sys
from pathlib import Path

def log_path() -> Path:
    """
    Returns the path to the log folder

    Returns:
        Path: The path to the log folder
    """
    system = platform.system()
    if system == "Windows":
        p = Path.home() / "AppData" / "Local" / "c4_sign" / "log"
    elif system == "Linux":
        p = Path.home() / ".local" / "state" / "c4_sign"
    elif system == "Darwin":
        p = Path.home() / "Library" / "Logs" / "c4_sign"
    else:
        raise NotImplementedError(f"Platform {system} not supported")
    p.mkdir(parents=True, exist_ok=True)
    return p

def setup_logger():
    logger.remove(0)
    logger.add(sys.stderr, level="INFO")
    logger.add(log_path() / "c4_sign.log", level="DEBUG", rotation="00:30", retention="1 week", compression="gz")
