import gzip

from psflib.psf2 import PSF2Font

SOURCE = "/usr/share/kbd/consolefonts/default8x16.psfu.gz"
TARGET = "output/default8x16_reverse.psfu.gz"


with gzip.open(SOURCE, "rb") as istream:
    font = PSF2Font.read(istream)

    for i in range(len(font.bitmaps)):
        old = font.bitmaps[i]
        new = bytearray(old)
        size = font.header.width * font.header.height

        for idx in range(size):
            opposite_idx = size - idx - 1
            value = old[opposite_idx // 8] & (1 << (opposite_idx % 8)) != 0

            if value:
                new[idx // 8] |= 1 << (idx % 8)
            else:
                new[idx // 8] &= ~(1 << (idx % 8))

        font.bitmaps[i] = bytes(new)

    with gzip.open(TARGET, "wb") as ostream:
        font.write(ostream)
