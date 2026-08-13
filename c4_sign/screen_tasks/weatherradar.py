from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
import c4_sign.lib.assets

import requests
import gzip
import threading
import numpy
import colorsys

from time import sleep

from typing import List, Tuple
from queue import SimpleQueue
from datetime import datetime, UTC
from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
from PIL import Image
from loguru import logger

class WeatherRadar(ScreenTask):
    ignore = False
    title = "Radar"
    artist = "Mac Coleman"
    canonical_name = "WeatherRadar"

    __user_agent = {"User-Agent": "placeholder"}
    # mrms/ncep don't specify a necessary user agent like the NWS API does, but I figure I will anyways to be nice.
    __sr_bref_dir = c4_sign.lib.assets.cache_path() / "radar" / "sr_bref"
    __sr_bvel_dir = c4_sign.lib.assets.cache_path() / "radar" / "sr_bvel"
    __sr_bref_url = "https://mrms.ncep.noaa.gov/RIDGEII/L3/KDVN/SR_BREF/"
    __sr_bvel_url = "https://mrms.ncep.noaa.gov/RIDGEII/L3/KDVN/SR_BVEL/"
    __capabilities_url = "https://opengeo.ncep.noaa.gov/geoserver/kdvn/ows?service=wms&version=1.3.0&request=GetCapabilities"

    __mv_latitude_degrees = 41.9219522
    __mv_longitude_degrees = -91.4168371
    __degrees_of_latitude_to_feet = 364409 # https://www.starpath.com/calc/Distance%20Calculators/degree.html
    __degrees_of_longitude_to_feet = 272152
    __32_miles_to_degrees_latitude = 32 * 5280 / __degrees_of_latitude_to_feet
    __32_miles_to_degrees_longitude = 32 * 5280 / __degrees_of_longitude_to_feet

    __frames_to_request = 25 # Show 5 frames per second for five seconds. Roughly 100 to 250 minutes of coverage.

    __downloader_thread = None
    __lock = threading.Lock()
    __message_queue = SimpleQueue()
    __ready_to_run = False
    __task_lock_acquired = False # Necessary to make sure teardown only releases the lock if the task itself has the lock.

    __sr_bref_frames: List[Tuple[Image.Image, str]]
    __sr_bvel_frames: List[Tuple[Image.Image, str]]

    __replays = 3 # The number of times to replay the radar sequence
    
    def __init__(self):
        logger.info("Starting RadarDownloader thread.")
        WeatherRadar.__downloader_thread = threading.Thread(target=WeatherRadar.__refresh_radar_images_thread, name="RadarImageDownloader", daemon=True, args=[WeatherRadar.__message_queue])
        WeatherRadar.__downloader_thread.start()

        self.frame = 0
        self.__display_state = "map"
        # Display stats
        # "map" -> 2.5 seconds
        # "labelfadeout" -> 1 seconds
        # "radarfadein" -> 1.5 seconds
        # "reflectivity" -> 3 replays
        # "velocity" -> 3 replays
        self.__top_text = ""
        self.__bottom_text = ""
        super().__init__()

    def __refresh_radar_images_thread(queue: SimpleQueue):
        logger.info("RadarDownloader thread started.")
        while True:
            try:
                WeatherRadar.__sr_bref_dir.mkdir(parents=True, exist_ok=True)
                WeatherRadar.__sr_bvel_dir.mkdir(parents=True, exist_ok=True)
                logger.info("RadarDownloader: Acquiring Bounding boxes.")
                bounding_box = WeatherRadar.__get_bounding_boxes()
                logger.success("RadarDownloader: Bounding boxes acquired.")
                WeatherRadar.__lock.acquire()
                logger.info("RadarDownloader: Acquiring SR_BREF images.")
                WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bref_url, WeatherRadar.__sr_bref_dir, True, bounding_box)
                logger.success("RadarDownloader: Acquired SR_BREF images.")
                logger.info("RadarDownloader: Acquiring SR_BVEL images.")
                WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bvel_url, WeatherRadar.__sr_bvel_dir, False, bounding_box)
                logger.success("RadarDownloader: Acquired SR_BVEL images.")
                WeatherRadar.__lock.release()

                # At least one set of images has been downloaded! The images can now be displayed!
                queue.put("ready")
            except Exception as e:
                logger.error(f"RadarDownloader: failed to download radar images.\n{str(e)}")
                WeatherRadar.__lock.release()
                queue.put("not ready")

            sleep(2 * 60) # Sleep for 2 minutes


    def __get_bounding_boxes() -> Tuple[float, float, float, float]:
        # left, top, right, bottom
        # west, north, east, south
        response = BeautifulSoup(requests.get(WeatherRadar.__capabilities_url, headers=WeatherRadar.__user_agent).text, "xml")
        bounding_box = response.find(lambda tag: tag.name == "Name" and "kdvn_sr_bref" in tag.text).parent.find("EX_GeographicBoundingBox")
        west = float(bounding_box.find("westBoundLongitude").text)
        east = float(bounding_box.find("eastBoundLongitude").text)
        south = float(bounding_box.find("southBoundLatitude").text)
        north = float(bounding_box.find("northBoundLatitude").text)
        return (west, north, east, south)
    
    def __filter_gray_pixels(r, g, b, a):
        # SR_BREF images tend to have lots of low-reflectivity clutter near the radar.
        # Unfortunately, Mount Vernon is pretty close to the Davenport radar, so there is a lot of gray pixels over the image.
        # This filter removes pixels that are mostly grey (low saturation)
        # However, areas of high reflectivity circle from red to white to pink, which means that particularly strong storms
        # have white pixels that would be removed by a simple saturation filter. These pixels are closer to white, so we will
        # just filter out grey ones by selecting pixels that have both low saturation and lower value than the white pixels.
        # I haven't really tested this extensively, but it seems to work okay on the images I have tested it on.
        # Only reflectivity images should be filtered, I think velocity images should not be filtered.
        saturation_threshold = 0.55
        value_threshold = .8
        hsv = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        if hsv[1] < saturation_threshold and hsv[2] < value_threshold:
            return r, g, b, 0
        else:
            return r, g, b, a

    def __check_and_download_radar_images(url: str, dir: Path, filter: bool, bounding_box: Tuple[float, float, float, float]) -> List[str]:
        # Download new radar images.
        # Fetch from URL like https://mrms.ncep.noaa.gov/RIDGEII/L3/KDVN/SR_BREF/
        # Parse file and download neccessary images
        # Fetch https://opengeo.ncep.noaa.gov/geoserver/kdvn/ows?service=wms&version=1.3.0&request=GetCapabilities
        # Parse file and use bounding box along with Mount Vernon's coordinates to determine coordinates of images to crop
        # Uncompress images
        # Crop, center, resize images
        # Delete old images
        images_list = BeautifulSoup(requests.get(url, headers=WeatherRadar.__user_agent).text, 'html.parser')
        anchor_tags = images_list.find_all('a')
        # Each element of links is of form (URL, future uncompressed filename, timestamp)
        all_links = [(anchor.get('href'), anchor.get('href').replace(".tif.gz", ".png"), anchor.parent.next_sibling.string.strip()) for anchor in images_list.find_all('a')[4:]]
        links = sorted(all_links, key=lambda x: x[1], reverse=True)[:WeatherRadar.__frames_to_request] # Sort by timestamp, most recent at the top

        need_to_download = []
        for link in links:
            if not (dir / link[1]).exists():
                need_to_download.append(link)

        # Delete files that are no longer needed
        existing_files = [f for f in dir.iterdir() if f.is_file()]
        for file in existing_files:
            if file.name not in [l[1] for l in links]:
                logger.debug(f"Going to delete: {file}")
                file.unlink(missing_ok=True)
        
        mv_bounding_box = (
            WeatherRadar.__mv_longitude_degrees - WeatherRadar.__32_miles_to_degrees_longitude,
            WeatherRadar.__mv_latitude_degrees + WeatherRadar.__32_miles_to_degrees_latitude,
            WeatherRadar.__mv_longitude_degrees + WeatherRadar.__32_miles_to_degrees_longitude,
            WeatherRadar.__mv_latitude_degrees - WeatherRadar.__32_miles_to_degrees_latitude
        )

        dim = 7407 # Resolution of the images (they are square!)
        img_width = int(dim * (mv_bounding_box[2]-mv_bounding_box[0])/(bounding_box[2]-bounding_box[0]))
        img_height = int(dim * (mv_bounding_box[1]-mv_bounding_box[3])/(bounding_box[1]-bounding_box[3]))
        img_left = int(dim * (mv_bounding_box[0]-bounding_box[0])/(bounding_box[2]-bounding_box[0]))
        img_top = int(dim * (bounding_box[1]-mv_bounding_box[1])/(bounding_box[1]-bounding_box[3]))

        vectorized_filter = numpy.vectorize(WeatherRadar.__filter_gray_pixels, otypes=[numpy.uint8, numpy.uint8, numpy.uint8, numpy.uint8])

        for image in need_to_download:
            logger.debug(f"Fetching {url + image[0]}")
            compressed = requests.get(url + image[0], headers=WeatherRadar.__user_agent).content
            # print(compressed[:200])
            with Image.open(BytesIO(gzip.decompress(compressed))) as tiff_image:
                resized_image = tiff_image.crop((img_left, img_top, img_left+img_width, img_top + img_height)).resize((32, 32), Image.Resampling.HAMMING)
                if filter:
                    array = numpy.array(resized_image)
                    red_channel, green_channel, blue_channel, alpha_channel = (
                        array[:, :, 0],
                        array[:, :, 1],
                        array[:, :, 2],
                        array[:, :, 3],
                    )
                    new_red, new_green, new_blue, new_alpha = vectorized_filter(red_channel, green_channel, blue_channel, alpha_channel)
                    resized_image = Image.fromarray(numpy.stack([new_red, new_green, new_blue, new_alpha], axis=-1), "RGBA")
                resized_image.save(str(dir / image[1]))

    def prepare(self):
        while not WeatherRadar.__message_queue.empty():
            if WeatherRadar.__message_queue.get_nowait() == "ready":
                WeatherRadar.__ready_to_run = True
            else:
                WeatherRadar.__ready_to_run = False

        if not WeatherRadar.__ready_to_run:
            logger.info("Radar images not ready, skipping.")
            return False
        
        locked = WeatherRadar.__lock.acquire(blocking=False)
        if not locked:
            logger.info("Failed to obtain radar image lock, skipping.")
            return False
        else:
            WeatherRadar.__task_lock_acquired = True
        
        self.frame = 0

        WeatherRadar.__sr_bref_frames = sorted([(Image.open(path), path.name) for path in WeatherRadar.__sr_bref_dir.iterdir() if path.is_file()], key=lambda x: x[1])

        interesting_pixels = 0
        for image in reversed(WeatherRadar.__sr_bref_frames):
            interesting_pixels += numpy.count_nonzero(numpy.array(image[0])[:,:,3])
            if interesting_pixels >= 0:
                break
        if interesting_pixels < 0:
            logger.info(f"There are no interesting radar images, skipping. Interesting pixels: {interesting_pixels}")
            WeatherRadar.__sr_bref_frames = None
            WeatherRadar.__lock.release()
            return False
        
        logger.info(f"{interesting_pixels} interesting pixels detected, running WeatherRadar")
        WeatherRadar.__sr_bvel_frames = sorted([(Image.open(path), path.name) for path in WeatherRadar.__sr_bvel_dir.iterdir() if path.is_file()], key=lambda x: x[1])
        return WeatherRadar.__ready_to_run and locked and super().prepare()
    
    def teardown(self, forced=False):
        WeatherRadar.__sr_bref_frames = None
        WeatherRadar.__sr_bvel_frames = None
        if WeatherRadar.__task_lock_acquired:
            WeatherRadar.__lock.release()
        return super().teardown(forced)

    def draw_frame(self, canvas, delta_time):
        radar_frame = self.frame // 5
        active_sequence = WeatherRadar.__sr_bref_frames if radar_frame < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else WeatherRadar.__sr_bvel_frames
        index = radar_frame % len(WeatherRadar.__sr_bref_frames) if radar_frame < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else (radar_frame - WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames)) % len(WeatherRadar.__sr_bvel_frames)
        # logger.info(f"fr: {self.frame}, i: {index}, bref: {active_sequence == WeatherRadar.__sr_bref_frames}, bvel: {active_sequence == WeatherRadar.__sr_bvel_frames}")
        d_str = active_sequence[index][1].split("_")[4]
        t_str = active_sequence[index][1].split("_")[5]
        t = datetime(int(d_str[0:4]), int(d_str[4:6]), int(d_str[6:8]), hour=int(t_str[0:2]), minute=int(t_str[2:4]), second=int(t_str[4:6]), tzinfo=UTC)
        self.__bottom_text = str(t.astimezone().time().strftime("%I:%M %p")).center(16)
        graphics.draw_image(canvas, 0, 0, numpy.array(active_sequence[index][0]))
        self.frame += 1
        return radar_frame > WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) + WeatherRadar.__replays * len(WeatherRadar.__sr_bvel_frames)
    
    def get_lcd_text(self):
        content = "Reflectivity" if self.frame // 5 < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else "Velocity"
        return content.center(16) + self.__bottom_text
