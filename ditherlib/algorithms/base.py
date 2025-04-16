from abc import ABC, abstractmethod
import numpy as np
from PIL import Image

class ErrorDiffusionDither(ABC):
    def __init__(self, threshold: int = 128, serpentine: bool = False):
        self.threshold = threshold
        self.serpentine = serpentine

    @abstractmethod
    def get_kernel(self):
        pass

    def dither(self, image: Image.Image) -> Image.Image:
        img_array = np.asarray(image.convert("L"), dtype=np.float32)
        height, width = img_array.shape
        kernel = self.get_kernel()

        for y in range(height):
            if self.serpentine and y % 2 == 1:
                # Right to left
                x_range = range(width - 1, -1, -1)
                dir_sign = -1
            else:
                # Left to right
                x_range = range(width)
                dir_sign = 1

            for x in x_range:
                old_val = img_array[y, x]
                new_val = 255.0 if old_val >= self.threshold else 0.0
                img_array[y, x] = new_val
                error = old_val - new_val

                for dx, dy, weight in kernel:
                    nx = x + dx * dir_sign
                    ny = y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        img_array[ny, nx] += error * weight

        img_array = np.clip(img_array, 0, 255).astype(np.uint8)
        return Image.fromarray(img_array, mode="L")
