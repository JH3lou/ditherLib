import numpy as np
from PIL import Image
from ditherlib.algorithms.atkinson import AtkinsonDither

def test_atkinson_on_midgray():
    # Create a 10x10 mid-gray image (value 128)
    data = np.full((10, 10), 128, dtype=np.uint8)
    img = Image.fromarray(data, mode="L")

    # Apply Atkinson dithering
    ditherer = AtkinsonDither()
    result = ditherer.dither(img)

    # Ensure result is binary (0 or 255 only)
    result_data = np.array(result)
    unique_values = np.unique(result_data)

    assert set(unique_values).issubset({0, 255}), f"Unexpected values: {unique_values}"
    assert 0 in unique_values and 255 in unique_values, "Expected both black and white pixels in dithered output"
