# Asset Loading

Throughout the course of your program, you might want to load a variety of files!
These might include videos, images, text files, or even subtitle files.
For example, the `bad_apple.py` task displays many images while running, which obviously must come from somewhere.

In order to avoid making people commit large files to Git (which can be an annoying process),
the C4 sign has a multitude of ways to download files, both from the internet and from the C4 google drive.

These files are cached so that the sign doesn't need to request new copies of the file every single time the task runs.
Instead, the files are discovered in the cache and loaded from there. This massively improves the speed of the sign.

This document describes the various ways of downloading files to the C4 sign and using them within your programs.

The functions below can be accessed by importing `c4_sign.lib.assets`:

```python
import c4_sign.lib.assets
```

## Table of Contents

1. [Asset Locations and Google Drive](#locations)
2. [Asset Functions](#assets)
   1. [cache_path](#cache_path)
   2. [get_ffmpeg](#get_ffmpeg)
   3. [video_to_images](#video_to_images)
   4. [image_from_url](#image_from_url)
   5. [resize_image](#resize_image)
   6. [file_from_url](#file_from_url)
   7. [file_from_google_drive](#google_drive)
3. [A note on debugging](#debugging)
4. [Examples](#examples)

# Asset Locations and Google Drive <a name="Locations"></a>

You can download files from any URL so long as it is available on the internet.
We recognize however that you might want to make your own files/resources to use in the sign!
For example, if you took your own picture or made a drawing you want to display, we need a way to get it on the sign without just trying to download it over the internet.
We've made a [Google Drive Folder](https://drive.google.com/drive/folders/1PweM5UME7iaHHXBA2m3Fbw3vI0Xlk5Fn) for this purpose.
If you need a file in your project that you can't just download from a URL, let us know and we'll add it to the Google drive folder!

# Asset Functions <a name="assets"></a>

## cache_path() <a name="cache_path"></a>

Returns a path to the cache of files.

| Value       | Datatype         | Description                             |
|-------------|------------------|-----------------------------------------|
| **return**  | `pathlib.Path`   | The path to the cache of saved files.   |

This behavior is system-dependent.
The following table illustrates where the cache is located.

| System    | Returned Path                                     |
|-----------|---------------------------------------------------|
| Windows   | `C:\Users\{username}\AppData\Local\c4_sign\cache` |
| Linux     | `/home/{username}/.cache/c4_sign/`                |
| Mac OS    | `/home/{username}/Library/Caches/c4_sign`         |

## get_ffmpeg() <a name="get_ffmpeg"></a>

Returns a path to `ffmpeg`, a command line tool for video/image encoding and modification.

| Value       | Datatype         | Description       |
|-------------|------------------|-------------------|
| **return**  | `pathlib.Path`   | Path to `ffmpeg`  |

## video_to_images(videoURL, resize=`True`) <a name="video_to_images"></a>

Downloads a video and converts it to a folder containing a sequence of images within the cache.
By default, it also resizes the downloaded images to be exactly 32 by 32 pixels (the size of our screen).
If the video has already been downloaded, it simply returns a path to the sequence of images.

| Value      | Datatype       | Description                                                                         |
|------------|----------------|-------------------------------------------------------------------------------------|
| videoURL   | `str`          | The url of the video.                                                               |
| resize     | `bool`         | Whether or not the downloaded images should be resized to 32x32. Defaults to `True` |
| **return** | `pathlib.Path` | The path to the saved images within the cache.                                      |

## image_from_url(url, resize=`True`) <a name="image_from_url"></a>
Downloads an image from a specified URL and saves it to the cache.
If the image is already in the cache, it will simply return the path to the image in the cache.
By default, resizes the image to 32x32 pixels, the size of the screen.

| Value      | Datatype       | Description                                                                        |
|------------|----------------|------------------------------------------------------------------------------------|
| url        | `str`          | The url of the image.                                                              |
| resize     | `bool`         | Whether or not the downloaded image should be resized to 32x32. Defaults to `True` |
| **return** | `pathlib.Path` | The path to the saved image within the cache.                                      |

## resize_image(image, size) <a name="resize_image"></a>
Resizes an image at a specified path and saves it back to the cache.
If you resize your images with one of the downloading functions above, you probably don't need this function.

| Value    | Datatype             | Description                                |
|----------|----------------------|--------------------------------------------|
| image    | `pathlib.Path`       | The path to the image in the cache.        |
| size     | `tuple[int, int]`    | The new size of the image (width, height). |

## file_from_url(url) <a name="file_from_url"></a>

Downloads a file from the specified URL.
If the file is already in the cache, it does not download it again.

| Value      | Datatype       | Description                                  |
|------------|----------------|----------------------------------------------|
| url        | `str`          | The url of the file.                         |
| **return** | `pathlib.Path` | The path to the saved file within the cache. |


## file_from_google_drive(path) <a name="google_drive"></a>

Downloads a file from the C4 Google Drive.
If the file is already in the cache, it does not download it again.

| Value      | Datatype       | Description                                   |
|------------|----------------|-----------------------------------------------|
| path       | `str`          | The path of the file within the google drive. |
| **return** | `pathlib.Path` | The path to the saved file within the cache.  |

# A note on debugging <a name="debugging"></a>

Please be aware that the cache *stores* the files you download so that the sign does not have to download the same files multiple times.
If you are writing a display task that relies on these functions, and the downloaded resources are not as you expect them to be, you must clear your cache and retry.
For example, if you are trying to use downloaded images, but they seem to be the wrong size, this may be caused by a bug in your code the first time you ran the simulator.
Even if you fixed the original bug, the cached version will still have the bugged files, so you need to delete your cache before you run the simulator again.

You can clear your cache by going to the following locations on your machine and deleting the misbehaving files,
or by completely emptying them.

| System    | Cache Path                                        |
|-----------|---------------------------------------------------|
| Windows   | `C:\Users\{username}\AppData\Local\c4_sign\cache` |
| Linux     | `/home/{username}/.cache/c4_sign/`                |
| Mac OS    | `/home/{username}/Library/Caches/c4_sign`         |

Please note that it will take some time to restart if you delete the cache, because the resources have to be redownloaded and stored in the cache again.

