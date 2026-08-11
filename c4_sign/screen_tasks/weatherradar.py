from c4_sign.base_task import ScreenTask
import c4_sign.lib.assets

import xml
import requests
import gzip

from typing import List, Tuple
from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
from PIL import Image

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
    
    def __init__(self):
        super().__init__()

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
                print(f"Going to delete: {file}")
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
            print(f"Fetching {url + image[0]}")
            compressed = requests.get(url + image[0], headers=WeatherRadar.__user_agent).content
            # print(compressed[:200])
            with Image.open(BytesIO(gzip.decompress(compressed))) as tiff_image:
                tiff_image.crop((img_left, img_top, img_left+img_width, img_top + img_height)).resize((32, 32), Image.Resampling.HAMMING).save(str(dir / image[1]))





    def prepare(self):
        # Repeat and do the same for SR_BVEL

        # Only run task if there are radar images that are not all transparent

        WeatherRadar.__sr_bref_dir.mkdir(parents=True, exist_ok=True)
        WeatherRadar.__sr_bvel_dir.mkdir(parents=True, exist_ok=True)
        bounding_box = WeatherRadar.__get_bounding_boxes()
        WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bref_url, WeatherRadar.__sr_bref_dir, bounding_box)
        WeatherRadar.__check_and_download_radar_images(WeatherRadar.__sr_bvel_url, WeatherRadar.__sr_bvel_dir, bounding_box)

    def draw_frame(self, canvas, delta_time):
        pass
