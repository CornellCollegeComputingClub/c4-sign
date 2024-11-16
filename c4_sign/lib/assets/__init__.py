import json
import platform
import shutil
import subprocess
from pathlib import Path

import ffmpeg_downloader as ffdl
import gdown
from loguru import logger
import requests
import yt_dlp
from PIL import Image


def cache_path() -> Path:
    """
    Returns the path to the cache folder

    Returns:
        Path: The path to the cache folder
    """
    system = platform.system()
    if system == "Windows":
        p = Path.home() / "AppData" / "Local" / "c4_sign" / "cache"
    elif system == "Linux":
        p = Path.home() / ".cache" / "c4_sign"
    elif system == "Darwin":
        p = Path.home() / "Library" / "Caches" / "c4_sign"
    else:
        raise NotImplementedError(f"Platform {system} not supported")
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_ffmpeg():
    if not ffdl.installed():
        from argparse import Namespace

        from ffmpeg_downloader.__main__ import install as ffdl_install

        n = Namespace()
        n.proxy = None
        n.retries = 5
        n.timeout = 15
        n.no_cache_dir = False
        n.upgrade = True
        n.y = True
        n.add_path = False
        n.no_simlinks = True
        n.set_env = None
        n.reset_env = False
        n.presets = None
        n.version = None
        n.force = False
        logger.info("Installing FFmpeg...")
        ffdl_install(n)
        logger.info("FFmpeg installed!")
    return ffdl.ffmpeg_path


def video_to_images(videoURL, resize=True):
    """
    Downloads a video from a URL and converts it to images

    Args:
        videoURL (str): The URL of the video
        resize (bool, optional): Whether to resize the images to 32x32. Defaults to True.

    Returns:
        Path: The path to the folder containing the images
    """
    cached_value = __check_cache(videoURL)
    if cached_value:
        return cached_value
    else:
        folder = __download_video(videoURL)
        if resize:
            logger.info("Resizing images for {}", videoURL)
            for image in folder.iterdir():
                resize_image(image, (32, 32))
        return folder


def image_from_url(url, resize=True):
    """
    Retrieves an image from the given URL and optionally resizes it.

    Args:
        url (str): The URL of the image.
        resize (bool, optional): Whether to resize the image. Defaults to True.

    Returns:
        PIL.Image.Image: The retrieved image.

    """
    cached_value = __check_cache(url)
    if cached_value:
        return cached_value
    else:
        image = file_from_url(url)
        if resize:
            resize_image(image, (32, 32))
        return image


def resize_image(image: Path, size: tuple[int, int]):
    """
    Resize the given image to the specified size.

    Args:
        image (Path): The path to the image file.
        size (tuple[int, int]): The desired size of the image (width, height).

    Returns:
        None
    """
    with Image.open(image) as img:
        img = img.resize(size)
        img.save(image)


def file_from_url(url):
    """
    Downloads a file from the given URL if it is not already cached, and returns the file path.

    Args:
        url (str): The URL of the file to download.

    Returns:
        str: The file path of the downloaded file.

    """
    cached_value = __check_cache(url)
    if cached_value:
        return cached_value
    else:
        return __download_file(url)


def file_from_google_drive(path):
    # first, check if we have the file locally
    # google drive files are stored in the cache/google_drive folder
    cache = cache_path()
    file = cache / "google_drive" / path
    if file.exists():
        return file
    # if we don't have the file, redownload the folder from google drive
    # and return the file
    else:
        return __download_google_drive_file(path)


def __download_google_drive_file(path):
    # download the folder from google drive
    folder = cache_path() / "google_drive"
    url = "https://drive.google.com/drive/folders/1PweM5UME7iaHHXBA2m3Fbw3vI0Xlk5Fn"
    logger.info("Downloading google drive folder")
    gdown.download_folder(url, output=str(folder), quiet=False)
    logger.debug("Google drive folder downloaded")
    # return the file
    file = folder / path
    if file.exists():
        return file
    else:
        logger.error("File {} not found in google drive folder!", path)
        raise FileNotFoundError(f"File {path} not found in google drive folder!")


def purge_cache():
    """
    Purges the cache directory.
    """
    logger.info("Purging cache")
    cache = cache_path()
    shutil.rmtree(cache)
    logger.info("Cache purged!")


def __download_file(url):
    logger.info("Downloading file from {}", url)
    cache = cache_path()
    image = requests.get(url, stream=True)
    filename = Path(url.split("/")[-1])
    filename = cache / filename
    with filename.open("wb") as f:
        for chunk in image.iter_content(chunk_size=8192):
            f.write(chunk)
    __write_cache(url, filename)
    return filename


def __check_cache(url):
    cache = cache_path()
    try:
        with open(cache / "cache.json", "r") as f:
            cache = json.load(f)
            if url in cache:
                return Path(cache[url])
            else:
                return None
    except FileNotFoundError:
        with open(cache / "cache.json", "w") as f:
            json.dump({}, f)
        return None


def __write_cache(url, path):
    cache = cache_path()
    with open(cache / "cache.json", "r") as f:
        cache_data = json.load(f)
    cache_data[url] = str(path)
    with open(cache / "cache.json", "w") as f:
        json.dump(cache_data, f)


def __format_selector(ctx):
    # formats are already sorted worst to best
    # so, we want *basically* the worst format
    # that is still a video (ofc)
    formats = ctx.get("formats")
    worst_video = next(f for f in formats if (f["vcodec"] != "none" and f["acodec"] == "none"))
    audio_ext = {"mp4": "m4a", "webm": "webm"}[worst_video["ext"]]
    worst_audio = next(
        f for f in formats if (f.get("acodec", "none") != "none" and f["vcodec"] == "none" and f["ext"] == audio_ext)
    )

    logger.debug("Selected formats: {}", [worst_video, worst_audio])

    yield {
        "format_id": f'{worst_video["format_id"]}+{worst_audio["format_id"]}',
        "ext": worst_video["ext"],
        "requested_formats": [worst_video, worst_audio],
        "protocol": f'{worst_video["protocol"]}+{worst_audio["protocol"]}',
    }


def __download_video(videoURL):
    logger.info("Downloading video from {}", videoURL)
    cache = cache_path()
    filename = None

    def __filename_hook(d):
        nonlocal filename
        if d["status"] == "finished":
            filename = Path(d["info_dict"]["filename"])

    with yt_dlp.YoutubeDL(
        {
            "format": __format_selector,
            "fragment_retries": 6,
            "noprogress": True,
            "outtmpl": str(cache / "%(id)s.%(ext)s"),
            "quiet": True,
            "retries": 3,
            "progress_hooks": [__filename_hook],
        }
    ) as ydl:
        logger.debug("Downloading video")
        ydl.download([videoURL])

    image_folder = cache / filename.stem
    image_folder.mkdir()
    # get ffmpeg
    ffmpeg = get_ffmpeg()
    # convert video to images
    logger.debug("Converting video to images")
    subprocess.run([ffmpeg, "-i", filename, "-vf", "fps=24", f"{image_folder}/%d.png"], check=True)
    # save to cache
    __write_cache(videoURL, image_folder)
    return image_folder
