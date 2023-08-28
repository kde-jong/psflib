from dataclasses import dataclass
from typing import BinaryIO

from .common import InvalidDataException, UnicodeDescription


@dataclass
class PSF1Header:
    MAGIC = bytes([0x36, 0x04])

    mode: int
    char_size: int

    @classmethod
    def read(cls, stream: BinaryIO):
        if stream.read(2) != cls.MAGIC:
            raise InvalidDataException("Wrong magic")

        return PSF1Header(
            _read_uchar(stream),  # mode
            _read_uchar(stream),  # char_size
        )

    def write(self, stream: BinaryIO):
        stream.write(self.MAGIC)
        _write_uchar(stream, self.mode)
        _write_uchar(stream, self.char_size)


class PSF1UnicodeDescription(UnicodeDescription):
    CHAR_SIZE = 2
    CHAR_ENCODING = "utf-16-le"
    SEPARATOR = bytes([0xFF, 0xFF])
    SEQUENCE_START = bytes([0xFF, 0xFE])


@dataclass
class PSF1Font:
    MODE_512 = 0x01
    MODE_HAS_TABLE = 0x02
    MODE_HAS_SEQUENCE = 0x04
    MAX_MODE = 0x05

    header: PSF1Header
    bitmaps: list[bytes]
    unicode_table: list[PSF1UnicodeDescription]

    @classmethod
    def read(cls, stream: BinaryIO):
        header = PSF1Header.read(stream)
        if header.mode > PSF1Font.MAX_MODE:
            raise InvalidDataException(
                f"Header mode ({header.mode}) is greater than maximum mode ({cls.MAX_MODE})"
            )

        length = 512 if header.mode & PSF1Font.MODE_512 else 256
        bitmaps: list[bytes] = list()
        for _ in range(length):
            bitmaps.append(stream.read(header.char_size))

        if not header.mode & (PSF1Font.MODE_HAS_TABLE | PSF1Font.MODE_HAS_SEQUENCE):
            return PSF1Font(header, bitmaps, list())

        unicode_table = list()
        for _ in range(length):
            unicode_table.append(PSF1UnicodeDescription.read(stream))

        return PSF1Font(header, bitmaps, unicode_table)

    def write(self, stream: BinaryIO):
        self.header.write(stream)

        length = 512 if self.header.mode & PSF1Font.MODE_512 else 256
        for i in range(length):
            stream.write(self.bitmaps[i])

        if not self.header.mode & PSF1Font.MODE_HAS_TABLE:
            return
        for i in range(length):
            self.unicode_table[i].write(stream)


def _read_uchar(stream: BinaryIO) -> int:
    return int.from_bytes(stream.read(1), byteorder="little", signed=False)


def _write_uchar(stream: BinaryIO, uint: int):
    stream.write(uint.to_bytes(1, byteorder="little", signed=False))
