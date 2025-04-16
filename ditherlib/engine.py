from PIL import Image
from ditherlib.algorithms.floyd_steinberg import FloydSteinbergDither
from ditherlib.algorithms.burkes import BurkesDither
from ditherlib.algorithms.stucki import StuckiDither
from ditherlib.algorithms.sierra import Sierra3Dither, Sierra2Dither, SierraLiteDither
from ditherlib.algorithms.atkinson import AtkinsonDither
from ditherlib.config import get_ditherer
from ditherlib.utils import load_image, save_image, convert_to_grayscale

DITHER_ALGORITHMS = {
    "floyd_steinberg": FloydSteinbergDither,
    "burkes": BurkesDither,
    "stucki": StuckiDither,
    "sierra_3": Sierra3Dither,
    "sierra_2": Sierra2Dither,
    "sierra_lite": SierraLiteDither,
    "atkinson": AtkinsonDither,
}

def apply_dithering(input_path: str, output_path: str, algorithm: str = "floyd_steinberg", threshold: int = 128):
    if algorithm not in DITHER_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}. Choose from: {list(DITHER_ALGORITHMS.keys())}")

    img = load_image(input_path)
    img = convert_to_grayscale(img)
    ditherer = get_ditherer(algorithm, threshold=threshold)
    result = ditherer.dither(img)
    save_image(result, output_path)
    print(f"Saved dithered image to: {output_path}")
