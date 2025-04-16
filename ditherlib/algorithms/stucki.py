from ditherlib.algorithms.base import ErrorDiffusionDither
from ditherlib.algorithms.kernels import KERNELS

class StuckiDither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128):
        super().__init__(threshold)

    def get_kernel(self):
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["stucki"].items()]

