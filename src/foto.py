from typing import Dict, Optional, Tuple
import reverse_geocode
import datetime as dt


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

        hash_ = self.meta.get("File:CurrentIPTCDigest")
        if not hash_:
            hash_ = str(hash(self.path.read_bytes()))

        self._file_hash = hash_
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

        datetime = self.meta.get("EXIF:CreateDate")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, "%Y:%m:%d %H:%M:%S")
            return self._datetime

        # try other fallback dates
        meta = self.exif.get_metadata(self.path)

        datetime = meta.get("RIFF:DateCreated")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, "%Y:%m:%d")
            return self._datetime

        datetime = meta.get("Composite:DateTimeOriginal")
        if datetime:
            self._datetime = dt.datetime.strptime(datetime, "%Y:%m:%d %H:%M:%S")
            return self._datetime

        # use file modify if nothing helps
        datetime = meta.get("File:FileModifyDate")
        datetime = dt.datetime.strptime(datetime, "%Y:%m:%d %H:%M:%S%z")
        if datetime:
            self._datetime = datetime
            return self._datetime
