from PIL import Image
import numpy as np

def load_image(path: str) -> Image.Image:
    return Image.open(path)

def save_image(img: Image.Image, path: str):
    img.save(path)

def convert_to_grayscale(img: Image.Image) -> Image.Image:
    return img.convert("L")

def apply_gamma(image: Image.Image, gamma: float = 1.0) -> Image.Image:
    if gamma == 1.0:
        return image
    lut = [pow(i / 255., gamma) * 255 for i in range(256)]
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    return image.point(lut)

def normalize_blue_noise(blue_noise: np.ndarray) -> np.ndarray:
    # Normalize blue noise matrix to range [0, 255] for thresholding
    bn_min, bn_max = blue_noise.min(), blue_noise.max()
    if bn_max == bn_min:
        return np.zeros_like(blue_noise, dtype=np.uint8)
    scaled = 255 * (blue_noise - bn_min) / (bn_max - bn_min)
    return scaled.astype(np.uint8)
