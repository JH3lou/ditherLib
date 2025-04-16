```markdown
# DitherLib

A modern, extensible Python library and GUI for applying a wide range of dithering algorithms to grayscale images. Built with flexibility and performance in mind, it supports both classic and adaptive error diffusion techniques, and provides an intuitive GUI for visual experimentation.

## Features

- Classic dithering algorithms: Floyd-Steinberg, Burkes, Stucki, Sierra variants, Atkinson
- Custom adaptive dithering with configurable parameters
- Live preview in GUI
- Gamma correction and downscaling
- CLI and Python API access
- Real-time histogram and image processing (WIP)

## GUI Demo

Start the GUI:
```bash
python gui/app.py
```

Load an image, choose an algorithm, and adjust parameters like threshold, gamma, and scan direction.

## Installation

### Install via pip:
```bash
git clone https://github.com/JH3lou/ditherLib.git
cd ditherLib
pip install -e .
```

### Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest tests/
```

## Example Usage (Python API)

```python
from PIL import Image
import numpy as np
from ditherlib.config import get_ditherer

img = Image.open("photo.png").convert("L")
ditherer = get_ditherer("floyd-steinberg", threshold=128)
result = ditherer.dither(img)
result.save("output.png")
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENCE.md) file.
```
