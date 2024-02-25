import json
import platform
import shutil
import subprocess
from pathlib import Path

import requests
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
    return "ffmpeg"


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


def purge_cache():
    """
    Purges the cache directory.
    """
    cache = cache_path()
    shutil.rmtree(cache)


def __download_file(url):
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


def __download_video(videoURL):
    cache = cache_path()
    data = requests.post(
        "https://co.wuk.sh/api/json",
        json={
            "url": videoURL,
            "vCodec": "h264",
            "vQuality": "144",  # we're making this 32x32! we don't need high quality
            "isAudioMuted": "true",
        },
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    ).json()
    video = requests.get(data["url"], stream=True)
    # get filename from content-disposition
    filename = Path(video.headers["content-disposition"].split("filename=")[1].strip('"'))
    filename = cache / filename
    with filename.open("wb") as f:
        for chunk in video.iter_content(chunk_size=8192):
            f.write(chunk)
    image_folder = cache / filename.stem
    image_folder.mkdir()
    # get ffmpeg
    ffmpeg = get_ffmpeg()
    # convert video to images
    subprocess.run([ffmpeg, "-i", filename, "-vf", "fps=24", f"{image_folder}/%d.png"])
    # save to cache
    __write_cache(videoURL, image_folder)
    return image_folder
