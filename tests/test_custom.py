import numpy as np
from PIL import Image
from ditherlib.algorithms.custom import CustomAdaptiveDither

def test_custom_adaptive_dither_defaults():
    data = np.full((10, 10), 128, dtype=np.uint8)
    img = Image.fromarray(data, mode="L")
    ditherer = CustomAdaptiveDither()
    result = ditherer.dither(img)
    result_data = np.array(result)
    unique_values = np.unique(result_data)

    assert set(unique_values).issubset({0, 255}), f"Unexpected values: {unique_values}"
    assert 0 in unique_values and 255 in unique_values, "Expected both black and white pixels in dithered output"
