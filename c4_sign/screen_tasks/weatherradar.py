from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
import c4_sign.lib.assets

import requests
import gzip
import threading
import numpy

from time import sleep

from typing import List, Tuple
from queue import SimpleQueue
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

    __sr_bref_frames: List[Tuple[Image.Image, str]]
    __sr_bvel_frames: List[Tuple[Image.Image, str]]

    __replays = 3 # The number of times to replay the radar sequence
    
    def __init__(self):
        logger.info("Starting RadarDownloader thread.")
        WeatherRadar.__downloader_thread = threading.Thread(target=WeatherRadar.__refresh_radar_images_thread, name="RadarImageDownloader", daemon=True, args=[WeatherRadar.__message_queue])
        WeatherRadar.__downloader_thread.start()

        self.frame = 0
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
                WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bref_url, WeatherRadar.__sr_bref_dir, bounding_box)
                logger.success("RadarDownloader: Acquired SR_BREF images.")
                logger.info("RadarDownloader: Acquiring SR_BVEL images.")
                WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bvel_url, WeatherRadar.__sr_bvel_dir, bounding_box)
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

    def __check_and_download_radar_images(url: str, dir: Path, bounding_box: Tuple[float, float, float, float]) -> List[str]:
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

        for image in need_to_download:
            logger.debug(f"Fetching {url + image[0]}")
            compressed = requests.get(url + image[0], headers=WeatherRadar.__user_agent).content
            # print(compressed[:200])
            with Image.open(BytesIO(gzip.decompress(compressed))) as tiff_image:
                tiff_image.crop((img_left, img_top, img_left+img_width, img_top + img_height)).resize((32, 32), Image.Resampling.HAMMING).save(str(dir / image[1]))

    def prepare(self):
        while not WeatherRadar.__message_queue.empty():
            if WeatherRadar.__message_queue.get_nowait() == "ready":
                WeatherRadar.__ready_to_run = True
            else:
                WeatherRadar.__ready_to_run = False
        
        locked = WeatherRadar.__lock.acquire(blocking=False)
        if not WeatherRadar.__ready_to_run:
            logger.info("Radar images not ready, skipping.")
            return False
        if not locked:
            logger.info("Failed to obtain radar image lock, skipping.")
            return False
        
        self.frame = 0

        WeatherRadar.__sr_bref_frames = sorted([(Image.open(path), str(path)) for path in WeatherRadar.__sr_bref_dir.iterdir() if path.is_file()], key=lambda x: x[1])
        WeatherRadar.__sr_bvel_frames = sorted([(Image.open(path), str(path)) for path in WeatherRadar.__sr_bvel_dir.iterdir() if path.is_file()], key=lambda x: x[1])
        return WeatherRadar.__ready_to_run and locked and super().prepare()
    
    def teardown(self, forced=False):
        WeatherRadar.__sr_bref_frames = None
        WeatherRadar.__sr_bvel_frames = None
        WeatherRadar.__lock.release()
        return super().teardown(forced)

    def draw_frame(self, canvas, delta_time):
        radar_frame = self.frame // 5
        active_sequence = WeatherRadar.__sr_bref_frames if radar_frame < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else WeatherRadar.__sr_bvel_frames
        index = radar_frame % len(WeatherRadar.__sr_bref_frames) if radar_frame < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else (radar_frame - WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames)) % len(WeatherRadar.__sr_bvel_frames)
        # logger.info(f"fr: {self.frame}, i: {index}, bref: {active_sequence == WeatherRadar.__sr_bref_frames}, bvel: {active_sequence == WeatherRadar.__sr_bvel_frames}") 
        graphics.draw_image(canvas, 0, 0, numpy.array(active_sequence[index][0]))
        self.frame += 1
        return radar_frame > WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) + WeatherRadar.__replays * len(WeatherRadar.__sr_bvel_frames)
    
    def get_lcd_text(self):
        content = "Reflectivity" if self.frame // 5 < WeatherRadar.__replays * len(WeatherRadar.__sr_bref_frames) else "Velocity"
        return content.center(16) + " "*16
