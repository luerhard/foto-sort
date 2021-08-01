import datetime as dt
import hashlib
import logging
from typing import Dict
from typing import Optional
from typing import Tuple

import reverse_geocode
from PIL import Image
from PIL import UnidentifiedImageError

logger = logging.getLogger()


class Foto:

    exif_tags = [
        "EXIF:GPSLatitudeRef",
        "EXIF:GPSLatitude",
        "EXIF:GPSLongitude",
        "EXIF:GPSLongitudeRef",
        "EXIF:CreateDate",
        "File:CurrentIPTCDigest",
    ]

    def __init__(self, exif, path):
        self.path = path
        self.exif = exif
        self.meta = self._read_metadata()

        self._file_hash = None
        self._datetime = None

    def _read_metadata(self):
        return self.exif.get_tags(self.exif_tags, str(self.path))

    def file_hash(self):
        if self._file_hash:
            return self._file_hash

        try:
            with Image.open(self.path) as img:
                img = img.tobytes()
        except (UnidentifiedImageError, OSError):
            img = self.path.read_bytes()

        self._file_hash = hashlib.sha1(img).hexdigest()
        return self._file_hash

    def coordinates(self) -> Optional[Tuple[float, float]]:

        longitude = self.meta.get("EXIF:GPSLongitude")
        longitude_ref = self.meta.get("EXIF:GPSLongitudeRef")
        latitude = self.meta.get("EXIF:GPSLatitude")
        latitude_ref = self.meta.get("EXIF:GPSLatitudeRef")

        if not (longitude or latitude):
            return None

        if latitude_ref == "S":
            latitude *= -1

        if longitude_ref == "W":
            longitude *= -1

        return latitude, longitude

    def location(self) -> Dict[str, Optional[str]]:
        coords = self.coordinates()
        if not coords:
            return {"country": None, "city": None}

        loc = reverse_geocode.search([coords])
        return loc.pop()

    def datetime(self):
        if self._datetime:
            return self._datetime

        STD_FMT = "%Y:%m:%d %H:%M:%S"

        datetime = self.meta.get("EXIF:CreateDate")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, STD_FMT)
            return self._datetime

        datetime = self.meta.get("EXIF:DateTimeOriginal")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, STD_FMT)
            return self._datetime

        # try other fallback dates
        meta = self.exif.get_metadata(str(self.path))

        datetime = meta.get("RIFF:DateCreated")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, "%Y:%m:%d")
            return self._datetime

        datetime = meta.get("Composite:DateTimeOriginal")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, STD_FMT)
            return self._datetime
