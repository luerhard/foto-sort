import shutil
import sqlite3
from pathlib import Path

import exiftool
from tqdm import tqdm

from .foto import Foto


class FotoSort:
    INCLUDE_SUFFIX = {
        ".avi",
        ".bmp",
        ".jpeg",
        ".jpg",
        ".mov",
        ".mp4",
        ".mkv",
        ".png",
        ".wav",
        ".wmv",
        ".tif",
    }
    DB_FILENAME = ".hashtable.sqlite"

    def __init__(self, source, dest):
        self.source_path = Path(source)
        self.dest_path = Path(dest)
        self.dest_path.mkdir(parents=True, exist_ok=True)

        self.exiftool = exiftool.ExifTool()
        self.exiftool.start()

        self.db = self.db_connect()

    def db_connect(self):

        table_stmt = """
        CREATE TABLE IF NOT EXISTS hashmap (
        hash TEXT PRIMARY KEY
        )
        """

        con = sqlite3.connect(str(self.dest_path / self.DB_FILENAME))
        con.execute(table_stmt)
        con.commit()
        return con

    def close(self):
        self.exiftool.terminate()
        self.db.close()

    def foto_exists(self, photo):
        hash_ = photo.file_hash()
        query = f"SELECT 1 FROM hashmap WHERE hash = '{hash_}' LIMIT 1"
        exists = self.db.execute(query).fetchone()
        if not exists:
            return False
        return True

    def foto_insert(self, photo):
        hash_ = photo.file_hash()
        query = f"INSERT INTO hashmap VALUES ('{hash_}')"
        self.db.execute(query)
        self.db.commit()

    @staticmethod
    def non_conflicting_filename(path):
        if not path.is_file():
            return path
        i = 0
        while True:
            i += 1
            new = path.parent / (str(path.stem) + f"_{i}")
            new = new.with_suffix(path.suffix)
            if not new.is_file():
                return new

    def new_file_location(self, photo):

        file_path = self.dest_path
        date = photo.datetime()
        loc = photo.location()
        if date:
            file_path /= str(date.year)
            if loc["country"]:
                file_path = file_path / loc["country"]
                if loc["city"]:
                    file_path = file_path / loc["city"]
            else:
                rel_path = photo.path.relative_to(self.source_path).parent
                file_path = (file_path / "unknown") / rel_path

            filename = date.strftime("%Y_%m_%d_%H_%M_%S")
        else:
            rel_path = photo.path.relative_to(self.source_path).parent
            file_path = (file_path / "unknown") / rel_path
            filename = photo.path.name

        file_path.mkdir(parents=True, exist_ok=True)
        new = self.non_conflicting_filename(
            (file_path / filename).with_suffix(photo.path.suffix),
        )
        return new

    def foto_copy(self, photo):
        new_file = self.new_file_location(photo)
        try:
            shutil.copy2(photo.path, new_file)
        except:  # noqa: E722
            # no idea what error copy2 will throw, Docs are unspecific
            shutil.copy(photo.path, new_file)
        self.foto_insert(photo)

    def run(self):
        for file in tqdm(self.source_folder()):
            photo = Foto(self.exiftool, file)
            if not self.foto_exists(photo):
                self.foto_copy(photo)

    def iter_folder(self, path):
        for p in path.glob("**/*"):
            if p.suffix.lower() in self.INCLUDE_SUFFIX:
                yield p

    def source_folder(self):
        return self.iter_folder(self.source_path)

    def dest_folder(self):
        return self.iter_folder(self.dest_path)
