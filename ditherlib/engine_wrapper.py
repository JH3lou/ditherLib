from PIL import Image
import numpy as np
from ditherlib.engine import apply_dithering
from ditherlib.config import get_ditherer

def image_array_to_pil(img_array):
    mode = "L" if img_array.ndim == 2 else "RGB"
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8), mode)

def pil_to_image_array(pil_img):
    return np.array(pil_img.convert("RGB" if pil_img.mode != "L" else "L"), dtype=np.uint8)

def process_dither(
    image_array,
    algorithm="adaptive",
    threshold=128,
    gamma=1.0,
    downscale_percent=100,
    serpentine=False,
    propagate_fraction=1.0,
    blue_noise=None,
    blue_noise_strength=0.0,
):
    # Convert to PIL
    pil_img = image_array_to_pil(image_array)

    # Downscale if needed
    if downscale_percent < 100:
        w, h = pil_img.size
        new_size = (int(w * downscale_percent / 100), int(h * downscale_percent / 100))
        pil_img = pil_img.resize(new_size, Image.NEAREST)

    # Gamma correction
    if gamma != 1.0:
        arr = np.asarray(pil_img).astype(np.float32)
        arr = 255 * ((arr / 255) ** (1 / gamma))
        pil_img = image_array_to_pil(arr)

    # Apply dithering
    ditherer = get_ditherer(
        algorithm,
        threshold=threshold,
        serpentine=serpentine,
        propagate_fraction=propagate_fraction,
        blue_noise=blue_noise,
        blue_noise_strength=blue_noise_strength,
    )
    result_img = ditherer.dither(pil_img)

    # Return NumPy image
    return np.array(result_img)
