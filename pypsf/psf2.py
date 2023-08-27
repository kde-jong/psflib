from dataclasses import dataclass
from typing import BinaryIO, Optional

from .exceptions import InvalidDataException


@dataclass
class PSF2Header:
    MAGIC = bytes([0x72, 0xB5, 0x4A, 0x86])

    version: int
    header_size: int
    flags: int
    length: int
    char_size: int
    height: int
    width: int

    @classmethod
    def read(cls, stream: BinaryIO):
        if stream.read(4) != PSF2Header.MAGIC:
            raise InvalidDataException("Wrong magic")

        return PSF2Header(
            _read_uint(stream),  # version
            _read_uint(stream),  # header_size
            _read_uint(stream),  # flags
            _read_uint(stream),  # length
            _read_uint(stream),  # char_size
            _read_uint(stream),  # height
            _read_uint(stream),  # width
        )

    def write(self, stream: BinaryIO):
        stream.write(PSF2Header.MAGIC)
        _write_uint(stream, self.version)
        _write_uint(stream, self.header_size)
        _write_uint(stream, self.flags)
        _write_uint(stream, self.length)
        _write_uint(stream, self.char_size)
        _write_uint(stream, self.height)
        _write_uint(stream, self.width)


@dataclass
class TableEntry:
    SEPARATOR = bytes([0xFF])
    SEQUENCE_START = bytes([0xFE])

    symbols: str
    sequences: list[str]

    @classmethod
    def read(cls, stream: BinaryIO):
        symbols = bytearray()
        while True:
            data = stream.read(1)
            if data == TableEntry.SEPARATOR:
                return TableEntry(symbols.decode("utf-8"), list())
            elif data == TableEntry.SEQUENCE_START:
                break
            else:
                symbols.append(data[0])

        sequences = list()
        sequence = bytearray()
        while True:
            data = stream.read(1)
            if data == TableEntry.SEPARATOR or data == TableEntry.SEQUENCE_START:
                sequences.append(sequence.decode("utf-8"))
                sequence.clear()
            if data == TableEntry.SEPARATOR:
                return TableEntry(symbols.decode("utf-8"), sequences)
            elif data != TableEntry.SEQUENCE_START:
                sequence.append(data[0])

    def write(self, stream: BinaryIO):
        stream.write(self.symbols.encode("utf-8"))

        for seq in self.sequences:
            stream.write(TableEntry.SEQUENCE_START)
            stream.write(seq.encode("utf-8"))

        stream.write(TableEntry.SEPARATOR)


@dataclass
class PSF2Font:
    MAX_VERSION = 0
    FLAG_HAS_TABLE = 1 << 0

    header: PSF2Header
    bitmaps: list[bytes]
    unicode_table: list[TableEntry]

    @classmethod
    def read(cls, stream: BinaryIO):
        header = PSF2Header.read(stream)
        if header.version > PSF2Font.MAX_VERSION:
            raise InvalidDataException(
                f"Header version ({header.version}) is greater than maximum version ({cls.MAX_VERSION})"
            )

        bitmaps: list[bytes] = list()
        for _ in range(header.length):
            bitmaps.append(stream.read(header.char_size))

        if not header.flags & PSF2Font.FLAG_HAS_TABLE:
            return PSF2Font(header, bitmaps, list())

        unicode_table: list[TableEntry] = list()
        for _ in range(header.length):
            unicode_table.append(TableEntry.read(stream))

        return PSF2Font(header, bitmaps, unicode_table)

    def write(self, stream: BinaryIO):
        self.header.write(stream)

        for i in range(self.header.length):
            stream.write(self.bitmaps[i])

        if not self.header.flags & PSF2Font.FLAG_HAS_TABLE:
            return
        for i in range(self.header.length):
            self.unicode_table[i].write(stream)


def _read_uint(stream: BinaryIO) -> int:
    return int.from_bytes(stream.read(4), byteorder="little", signed=False)


def _write_uint(stream: BinaryIO, uint: int):
    stream.write(uint.to_bytes(4, byteorder="little", signed=False))
