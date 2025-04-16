from ditherlib.algorithms.base import ErrorDiffusionDither
from ditherlib.algorithms.kernels import KERNELS

class AtkinsonDither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128):
        super().__init__(threshold)

    def get_kernel(self):
        # Atkinson only propagates 3/4 of the error (handled in base class or externally if extended)
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["atkinson"].items()]
