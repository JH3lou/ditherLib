import numpy as np
from PIL import Image
from ditherlib.algorithms.stucki import StuckiDither

def _run_binary_output_test(ditherer_class):
    data = np.full((10, 10), 128, dtype=np.uint8)
    img = Image.fromarray(data, mode="L")
    ditherer = ditherer_class()
    result = ditherer.dither(img)
    result_data = np.array(result)
    unique_values = np.unique(result_data)
    assert set(unique_values).issubset({0, 255}), f"Unexpected values: {unique_values}"
    assert 0 in unique_values and 255 in unique_values, "Expected both black and white pixels in dithered output"

def test_stucki():
    _run_binary_output_test(StuckiDither)
