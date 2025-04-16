import numpy as np
from PIL import Image
from ditherlib.algorithms.base import ErrorDiffusionDither
from ditherlib.algorithms.kernels import KERNELS
from ditherlib.utils import normalize_blue_noise

class CustomAdaptiveDither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128, serpentine: bool = True, propagate_fraction: float = 1.0,
                 blue_noise: np.ndarray = None, blue_noise_strength: float = 0.0):
        super().__init__(threshold)
        self.serpentine = serpentine
        self.propagate_fraction = propagate_fraction
        self.blue_noise = normalize_blue_noise(blue_noise) if blue_noise is not None else None
        self.blue_noise_strength = blue_noise_strength

    def get_kernel(self):
        # Base kernel uses Two-Row Sierra for balance
        return [(1, 0, 4 / 16), (2, 0, 3 / 16),
                (-2, 1, 1 / 16), (-1, 1, 2 / 16), (0, 1, 3 / 16), (1, 1, 2 / 16), (2, 1, 1 / 16)]

    def dither(self, image: Image.Image) -> Image.Image:
        data = np.array(image, dtype=np.float32)
        height, width = data.shape
        kernel = self.get_kernel()

        for y in range(height):
            x_range = range(width) if not self.serpentine or y % 2 == 0 else range(width - 1, -1, -1)
            mirror = self.serpentine and y % 2 != 0

            for x in x_range:
                old_pixel = data[y, x]

                # Apply blue-noise threshold adjustment if enabled
                local_threshold = self.threshold
                if self.blue_noise is not None:
                    noise_val = self.blue_noise[y % self.blue_noise.shape[0], x % self.blue_noise.shape[1]]
                    local_threshold += (noise_val - 127.5) * (self.blue_noise_strength / 127.5)

                new_pixel = 255.0 if old_pixel >= local_threshold else 0.0
                data[y, x] = new_pixel
                error = (old_pixel - new_pixel) * self.propagate_fraction

                for dx, dy, weight in kernel:
                    dx = -dx if mirror else dx
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        data[ny, nx] += error * weight

        return Image.fromarray(np.clip(data, 0, 255).astype(np.uint8), mode="L")
