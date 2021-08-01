from pathlib import Path

import exiftool
import pytest

from fotosort.foto import Foto


@pytest.fixture
def original():
    return Path("tests/testdata/duplicates/original.jpg")


class TestFotoSort:
    @classmethod
    def setup_class(cls):
        cls.tool = exiftool.ExifTool()
        cls.tool.start()

    @classmethod
    def teardown_class(cls):
        cls.tool.terminate()

    def test_duplicate_hash(self, original):
        foto2 = Path("tests/testdata/duplicates/duplicate.jpg")
        f1 = Foto(self.tool, original)
        f2 = Foto(self.tool, foto2)
        assert f1.file_hash() == f2.file_hash()

    def test_metadata_independent_hash(self, original):
        foto2 = Path("tests/testdata/duplicates/duplicate_w_diff_metadata.jpg")
        f1 = Foto(self.tool, original)
        f2 = Foto(self.tool, foto2)
        assert f1.file_hash() == f2.file_hash()

    def test_different_files_hash(self, original):
        foto2 = Path("tests/testdata/duplicates/different.jpg")
        f1 = Foto(self.tool, original)
        f2 = Foto(self.tool, foto2)
        assert f1.file_hash() != f2.file_hash()

    def test_not_an_image_hash(self):
        foto = Path("tests/testdata/duplicates/empty_video.mkv")
        f = Foto(self.tool, foto)
        assert f.file_hash() == "282003a9cff7bbadb41fa05748c21775eb61dccd"
