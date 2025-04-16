from ditherlib.algorithms.base import ErrorDiffusionDither
from ditherlib.algorithms.kernels import KERNELS



class Sierra3Dither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128):
        super().__init__(threshold)

    def get_kernel(self):
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["sierra_3"].items()]


class Sierra2Dither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128):
        super().__init__(threshold)

    def get_kernel(self):
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["sierra_2"].items()]


class SierraLiteDither(ErrorDiffusionDither):
    def __init__(self, threshold: int = 128):
        super().__init__(threshold)

    def get_kernel(self):
        return [(dx, dy, weight) for (dx, dy), weight in KERNELS["sierra_lite"].items()]
