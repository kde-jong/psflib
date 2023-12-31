import gzip

from psflib.psf2 import PSF2Font

SOURCE = "/usr/share/kbd/consolefonts/default8x16.psfu.gz"
TARGET = "output/default8x16_inverse.psfu.gz"


with gzip.open(SOURCE, "rb") as file:
    font = PSF2Font.read(file)

bitmaps = [bytearray(bitmap) for bitmap in font.bitmaps]
for bitmap in bitmaps:
    for i in range(len(bitmap)):
        bitmap[i] ^= 0xFF
font.bitmaps = [bytes(bitmap) for bitmap in bitmaps]

with gzip.open(TARGET, "wb") as file:
    font.write(file)
