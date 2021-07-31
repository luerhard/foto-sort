from fotosort.foto import Foto
import exiftool
from pathlib import Path

def test_duplicate_hash():
    foto1 = Path("tests/testdata/duplicates/2018_10_24_14_10_38_1.jpg")
    foto2 = Path("tests/testdata/duplicates/2018_10_24_14_10_38.jpg")

    tool = exiftool.ExifTool()
    tool.start()

    f1 = Foto(tool, foto1)
    f2 = Foto(tool, foto2)

    assert f1.file_hash() == f2.file_hash()