from ditherlib.algorithms.base import ErrorDiffusionDither
from ditherlib.algorithms.kernels import KERNELS

class FloydSteinbergDither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128, serpentine: bool = False):
        super().__init__(threshold, serpentine)

    def get_kernel(self):
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["floyd_steinberg"].items()]
