from ditherlib.algorithms.floyd_steinberg import FloydSteinbergDither
from ditherlib.algorithms.burkes import BurkesDither
from ditherlib.algorithms.stucki import StuckiDither
from ditherlib.algorithms.sierra import Sierra3Dither, Sierra2Dither, SierraLiteDither
from ditherlib.algorithms.atkinson import AtkinsonDither
from ditherlib.algorithms.custom import CustomAdaptiveDither


# Future: register adaptive and custom algorithms here

def get_ditherer(name: str, threshold: int = 128, **kwargs):
    registry = {
        "floyd-steinberg": FloydSteinbergDither,
        "burkes": BurkesDither,
        "stucki": StuckiDither,
        "sierra-3": Sierra3Dither,
        "sierra-2": Sierra2Dither,
        "sierra-lite": SierraLiteDither,
        "atkinson": AtkinsonDither,
        "adaptive": CustomAdaptiveDither,
    }

    if name not in registry:
        raise ValueError(f"Unknown dithering algorithm: {name}")

    cls = registry[name]
    
    # Pass extended args only for CustomAdaptiveDither
    if cls is CustomAdaptiveDither:
        return cls(threshold=threshold, **kwargs)
    else:
        return cls(threshold=threshold)