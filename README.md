# psflib

A Python library for working with PC Screen Fonts

## Usage

```py
from psflib.psf2 import PSF2Font

with open("input_font.psfu", "rb") as file:
	font = PSF2Font.read(file)

# Do something with the data here

with open("output_font.psfu", "wb") as file:
	font.write(file)
```

View the examples [here](examples/).
