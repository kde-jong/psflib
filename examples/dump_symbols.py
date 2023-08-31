import gzip
import json

from psflib.psf2 import PSF2Font

SOURCE = "/usr/share/kbd/consolefonts/default8x16.psfu.gz"
TARGET = "output/default8x16_dump.json"

with gzip.open(SOURCE, "rb") as file:
    font = PSF2Font.read(file)

data = [entry.symbols for entry in font.unicode_table]

with open(TARGET, "w") as file:
    json.dump(data, file, indent=4)
