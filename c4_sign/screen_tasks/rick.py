import base64
import random
from datetime import timedelta

import numpy
import srt
from PIL import Image

from c4_sign.base_task import ScreenTask
from c4_sign.lib import graphics
from c4_sign.lib.assets import video_to_images

LYRICS = base64.b64decode(
    "MAowMDowMDoxOCw4MDAgLS0+IDAwOjAwOjIyLDYwMApXZSdyZSBubyBzdHJhbmdlcnMgdG8gbG92ZQoKMQowMDowMDoyMiw4MDAgLS0+IDAwOjAwOjI2LDcwMApZb3Uga25vdyB0aGUgcnVsZXMgYW5kIHNvIGRvIEkKCjIKMDA6MDA6MjYsOTAwIC0tPiAwMDowMDozMCw3MDAKQSBmdWxsIGNvbW1pdG1lbnQncyB3aGF0IEknbSB0aGlua2luZyBvZgoKMwowMDowMDozMCw5MDAgLS0+IDAwOjAwOjM0LDcwMApZb3Ugd291bGRuJ3QgZ2V0IHRoaXMgZnJvbSBhbnkgb3RoZXIgZ3V5Cgo0CjAwOjAwOjM0LDkwMCAtLT4gMDA6MDA6MzksNjAwCkkganVzdCB3YW50IHRvIHRlbGwgeW91IGhvdyBJJ20gZmVlbGluZwoKNQowMDowMDozOSw4MDAgLS0+IDAwOjAwOjQzLDEwMApHb3R0YSBtYWtlIHlvdSB1bmRlcnN0YW5kCgo2CjAwOjAwOjQzLDMwMCAtLT4gMDA6MDA6NDYsOTAwCk5ldmVyIGdvbm5hIGdpdmUgeW91IHVwLCBuZXZlcgpnb25uYSBsZXQgeW91IGRvd24KCjcKMDA6MDA6NDcsMTAwIC0tPiAwMDowMDo1MSw0MDAKTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQoKOAowMDowMDo1MSw2MDAgLS0+IDAwOjAwOjU1LDMwMApOZXZlciBnb25uYSBtYWtlIHlvdSBjcnksCm5ldmVyIGdvbm5hIHNheSBnb29kYnllCgo5CjAwOjAwOjU1LDUwMCAtLT4gMDA6MDE6MDAsNDAwCk5ldmVyIGdvbm5hIHRlbGwgYSBsaWUgYW5kIGh1cnQgeW91CgoxMAowMDowMTowMCw2MDAgLS0+IDAwOjAxOjA0LDQwMApXZSd2ZSBrbm93biBlYWNoIG90aGVyIGZvciBzbyBsb25nCgoxMQowMDowMTowNCw2MDAgLS0+IDAwOjAxOjA4LDgwMApZb3VyIGhlYXJ0J3MgYmVlbiBhY2hpbmcgYnV0CnlvdSdyZSB0b28gc2h5IHRvIHNheSBpdAoKMTIKMDA6MDE6MDksMDAwIC0tPiAwMDowMToxMiw5MDAKSW5zaWRlIHdlIGJvdGgga25vdyB3aGF0J3MgYmVlbiBnb2luZyBvbgoKMTMKMDA6MDE6MTMsMTAwIC0tPiAwMDowMToxNywxMDAKV2Uga25vdyB0aGUgZ2FtZSBhbmQgd2UncmUgZ29ubmEgcGxheSBpdAoKMTQKMDA6MDE6MTcsMzAwIC0tPiAwMDowMToyMiw2MDAKQW5kIGlmIHlvdSBhc2sgbWUgaG93IEknbSBmZWVsaW5nCgoxNQowMDowMToyMiw4MDAgLS0+IDAwOjAxOjI1LDMwMApEb24ndCB0ZWxsIG1lIHlvdSdyZSB0b28gYmxpbmQgdG8gc2VlCgoxNgowMDowMToyNSw1MDAgLS0+IDAwOjAxOjI5LDAwMApOZXZlciBnb25uYSBnaXZlIHlvdSB1cCwgbmV2ZXIKZ29ubmEgbGV0IHlvdSBkb3duCgoxNwowMDowMToyOSwyMDAgLS0+IDAwOjAxOjMzLDcwMApOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91CgoxOAowMDowMTozMyw5MDAgLS0+IDAwOjAxOjM3LDUwMApOZXZlciBnb25uYSBtYWtlIHlvdSBjcnksCm5ldmVyIGdvbm5hIHNheSBnb29kYnllCgoxOQowMDowMTozNyw3MDAgLS0+IDAwOjAxOjQxLDgwMApOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQoKMjAKMDA6MDE6NDIsMDAwIC0tPiAwMDowMTo0NiwwMDAKTmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAsIG5ldmVyCmdvbm5hIGxldCB5b3UgZG93bgoKMjEKMDA6MDE6NDYsMjAwIC0tPiAwMDowMTo1MCw2MDAKTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQoKMjIKMDA6MDE6NTAsODAwIC0tPiAwMDowMTo1NCw1MDAKTmV2ZXIgZ29ubmEgbWFrZSB5b3UgY3J5LApuZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQoKMjMKMDA6MDE6NTQsNzAwIC0tPiAwMDowMTo1OSw1MDAKTmV2ZXIgZ29ubmEgdGVsbCBhIGxpZSBhbmQgaHVydCB5b3UKCjI0CjAwOjAxOjU5LDcwMCAtLT4gMDA6MDI6MDMsNTAwCihPb2ggZ2l2ZSB5b3UgdXApCgoyNQowMDowMjowMyw3MDAgLS0+IDAwOjAyOjA4LDEwMAooT29oIGdpdmUgeW91IHVwKQoKMjYKMDA6MDI6MDgsMzAwIC0tPiAwMDowMjoxMSw5MDAKKE9vaCkgTmV2ZXIgZ29ubmEgZ2l2ZSwgbmV2ZXIKZ29ubmEgZ2l2ZSAoZ2l2ZSB5b3UgdXApCgoyNwowMDowMjoxMiwxMDAgLS0+IDAwOjAyOjE2LDEwMAooT29oKSBOZXZlciBnb25uYSBnaXZlLCBuZXZlcgpnb25uYSBnaXZlIChnaXZlIHlvdSB1cCkKCjI4CjAwOjAyOjE2LDMwMCAtLT4gMDA6MDI6MjAsNTAwCldlJ3ZlIGtub3duIGVhY2ggb3RoZXIgZm9yIHNvIGxvbmcKCjI5CjAwOjAyOjIwLDcwMCAtLT4gMDA6MDI6MjQsODAwCllvdXIgaGVhcnQncyBiZWVuIGFjaGluZyBidXQKeW91J3JlIHRvbyBzaHkgdG8gc2F5IGl0CgozMAowMDowMjoyNSwwMDAgLS0+IDAwOjAyOjI5LDAwMApJbnNpZGUgd2UgYm90aCBrbm93IHdoYXQncyBiZWVuIGdvaW5nIG9uCgozMQowMDowMjoyOSwyMDAgLS0+IDAwOjAyOjMzLDIwMApXZSBrbm93IHRoZSBnYW1lIGFuZCB3ZSdyZSBnb25uYSBwbGF5IGl0CgozMgowMDowMjozMyw0MDAgLS0+IDAwOjAyOjM3LDYwMApJIGp1c3Qgd2FudCB0byB0ZWxsIHlvdSBob3cgSSdtIGZlZWxpbmcKCjMzCjAwOjAyOjM3LDgwMCAtLT4gMDA6MDI6NDEsMTAwCkdvdHRhIG1ha2UgeW91IHVuZGVyc3RhbmQKCjM0CjAwOjAyOjQxLDMwMCAtLT4gMDA6MDI6NDUsMTAwCk5ldmVyIGdvbm5hIGdpdmUgeW91IHVwLCBuZXZlcgpnb25uYSBsZXQgeW91IGRvd24KCjM1CjAwOjAyOjQ1LDMwMCAtLT4gMDA6MDI6NDksMzAwCk5ldmVyIGdvbm5hIHJ1biBhcm91bmQgYW5kIGRlc2VydCB5b3UKCjM2CjAwOjAyOjQ5LDUwMCAtLT4gMDA6MDI6NTMsNzAwCk5ldmVyIGdvbm5hIG1ha2UgeW91IGNyeSwKbmV2ZXIgZ29ubmEgc2F5IGdvb2RieWUKCjM3CjAwOjAyOjUzLDkwMCAtLT4gMDA6MDI6NTcsODAwCk5ldmVyIGdvbm5hIHRlbGwgYSBsaWUgYW5kIGh1cnQgeW91CgozOAowMDowMjo1OCwwMDAgLS0+IDAwOjAzOjAyLDAwMApOZXZlciBnb25uYSBnaXZlIHlvdSB1cCwgbmV2ZXIKZ29ubmEgbGV0IHlvdSBkb3duCgozOQowMDowMzowMiwyMDAgLS0+IDAwOjAzOjA2LDEwMApOZXZlciBnb25uYSBydW4gYXJvdW5kIGFuZCBkZXNlcnQgeW91Cgo0MAowMDowMzowNiwzMDAgLS0+IDAwOjAzOjEwLDQwMApOZXZlciBnb25uYSBtYWtlIHlvdSBjcnksCm5ldmVyIGdvbm5hIHNheSBnb29kYnllCgo0MQowMDowMzoxMCw2MDAgLS0+IDAwOjAzOjE1LDEwMApOZXZlciBnb25uYSB0ZWxsIGEgbGllIGFuZCBodXJ0IHlvdQoKNDIKMDA6MDM6MTUsMzAwIC0tPiAwMDowMzoxOCw4MDAKTmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXAsIG5ldmVyCmdvbm5hIGxldCB5b3UgZG93bgoKNDMKMDA6MDM6MTksMDAwIC0tPiAwMDowMzoyMywyMDAKTmV2ZXIgZ29ubmEgcnVuIGFyb3VuZCBhbmQgZGVzZXJ0IHlvdQoKNDQKMDA6MDM6MjMsNDAwIC0tPiAwMDowMzoyNywzMDAKTmV2ZXIgZ29ubmEgbWFrZSB5b3UgY3J5LApuZXZlciBnb25uYSBzYXkgZ29vZGJ5ZQoKNDUKMDA6MDM6MjcsNTAwIC0tPiAwMDowMzozMiw1MDAKTmV2ZXIgZ29ubmEgdGVsbCBhIGxpZSBhbmQgaHVydCB5b3UKCjQ2CjAwOjAzOjMzLDUwMCAtLT4gMDA6MDM6NDIsNTAwCnd3dy5SZW50QW5BZHZpc2VyLmNvbQoK"
)


class RickRoll(ScreenTask):
    title = "Rick Roll"
    artist = "Luna"

    def __init__(self):
        super().__init__(timedelta(seconds=1), timedelta(hours=1))  # :)
        self.prepare_bad_apple()

    def prepare_bad_apple(self):
        # this'll take a bit...
        # first, we need to load the video and split it into frames
        # then we need to convert each frame into a 32x32 image
        # ...yeah. fortunately, we can cache this!
        image_folder_path = video_to_images("https://www.youtube.com/watch?v=fH64whs5tzI")
        self.image_folder_path = image_folder_path
        self.subtitles = list(srt.parse(LYRICS.decode()))

    def prepare(self):
        # weighted random choice, we want a 2% chance of the full video
        self.stop = False
        self.frame = 1
        return random.random() < 0.02

    def get_lcd_text(self) -> str:
        current_time = self.frame * (1 / 24)
        for subtitle in self.subtitles:
            if subtitle.start.total_seconds() < current_time < subtitle.end.total_seconds():
                content = subtitle.content.ljust(32)
                if len(content) > 32:
                    # add ... to the end
                    content = content[:29] + "..."
                return content
        return super().get_lcd_text()

    def draw_frame(self, canvas, delta_time):
        # we need to load the image
        image = Image.open(self.image_folder_path / f"{self.frame}.png")
        graphics.draw_image(canvas, 0, 0, numpy.array(image))
        self.frame += 1
        if self.frame > 5088:
            self.frame = 1
            self.stop = True
        return self.stop
