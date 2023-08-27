import gzip
import io
import os
from typing import BinaryIO
from unittest import TestCase

from pypsf.psf1 import PSF1Header
from pypsf.psf2 import PSF2Font, PSF2Header


def peek(stream: BinaryIO, n: int) -> bytes:
    result = stream.read(n)
    stream.seek(0)
    return result


class TestFonts(TestCase):
    def _test_psf2(self, path: str, stream: BinaryIO):
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
                if peek(stream, 2) == PSF1Header.MAGIC:
                    # self._test_psf1()
                    pass
                elif peek(stream, 4) == PSF2Header.MAGIC:
                    self._test_psf2(path, stream)
