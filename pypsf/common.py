from dataclasses import dataclass, field
from typing import BinaryIO


class InvalidDataException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


@dataclass
class UnicodeDescription:
    CHAR_SIZE: int = field(init=False)
    CHAR_ENCODING: str = field(init=False)
    SEPARATOR: bytes = field(init=False)
    SEQUENCE_START: bytes = field(init=False)

    symbols: str
    sequences: list[str]

    @classmethod
    def read(cls, stream: BinaryIO):
        symbols = bytearray()
        while True:
            data = stream.read(cls.CHAR_SIZE)
            if data == cls.SEPARATOR:
                return cls(symbols.decode(cls.CHAR_ENCODING), list())
            elif data == cls.SEQUENCE_START:
                break
            else:
                for byte in data:
                    symbols.append(byte)

        sequences = list()
        sequence = bytearray()
        while True:
            data = stream.read(cls.CHAR_SIZE)
            if data == cls.SEPARATOR or data == cls.SEQUENCE_START:
                sequences.append(sequence.decode(cls.CHAR_ENCODING))
                sequence.clear()
            if data == cls.SEPARATOR:
                return cls(symbols.decode(cls.CHAR_ENCODING), sequences)
            elif data != cls.SEQUENCE_START:
                for byte in data:
                    sequence.append(byte)

    def write(self, stream: BinaryIO):
        stream.write(self.symbols.encode(self.CHAR_ENCODING))

        for seq in self.sequences:
            stream.write(self.SEQUENCE_START)
            stream.write(seq.encode(self.CHAR_ENCODING))

        stream.write(self.SEPARATOR)
