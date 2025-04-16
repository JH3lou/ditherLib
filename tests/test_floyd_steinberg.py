import numpy as np
from PIL import Image
from ditherlib.algorithms.floyd_steinberg import FloydSteinbergDither

def test_floyd_steinberg_on_midgray():
    # Create a 10x10 mid-gray image (value 128)
    data = np.full((10, 10), 128, dtype=np.uint8)
    img = Image.fromarray(data, mode="L")

    # Apply Floyd–Steinberg dithering
    ditherer = FloydSteinbergDither()
    result = ditherer.dither(img)

    # Ensure result is binary (0 or 255 only)
    result_data = np.array(result)
    unique_values = np.unique(result_data)

    assert set(unique_values).issubset({0, 255}), f"Unexpected values: {unique_values}"

    # Sanity check: expect some black and white pixels
    assert 0 in unique_values and 255 in unique_values, "Expected both black and white pixels in dithered output"
