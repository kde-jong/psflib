import gzip
import io
import os
from typing import BinaryIO
from unittest import TestCase

from pypsf import psf1
from pypsf.psf2 import PSF2Font


class TestPSF2(TestCase):
    def _test_file(self, path: str, stream: BinaryIO):
        font = PSF2Font.read(stream)

        self.assertEqual(
            len(stream.read()),
            0,
            f"Did not read file {path} through to the very end (total size is {stream.tell()})",
        )

        self.assertEqual(len(font.bitmaps), font.header.length)
        if font.header.flags & PSF2Font.HAS_UNICODE_TABLE:
            self.assertEqual(len(font.unicode_table), font.header.length)
        else:
            self.assertIsNone(font.unicode_table)

        clone = io.BytesIO()
        font.write(clone)

        stream.seek(0)
        clone.seek(0)
        self.assertEqual(
            stream.read(), clone.read(), "Written bytes not the same as read bytes"
        )

    def test_kbd_fonts(self):
        ROOT = "/usr/share/kbd/consolefonts/"

        for path in os.listdir(ROOT):
            if not path.endswith(".psfu.gz"):
                continue

            with gzip.open(ROOT + path, "rb") as stream:
                if stream.read(2) == psf1.PSF1_MAGIC:
                    continue
                stream.seek(0)

                self._test_file(ROOT + path, stream)
