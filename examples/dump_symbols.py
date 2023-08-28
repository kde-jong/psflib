import gzip
import json

from pypsf.psf2 import PSF2Font

SOURCE = "/usr/share/kbd/consolefonts/default8x16.psfu.gz"
TARGET = "output/default8x16_dump.json"

with gzip.open(SOURCE, "rb") as istream:
    font = PSF2Font.read(istream)

    data = [entry.symbols for entry in font.unicode_table]

    with open(TARGET, "w") as ostream:
        json.dump(data, ostream, indent=4)
