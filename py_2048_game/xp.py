import numpy as np
xp = np

try:
    import cupy as cp
    xp = cp
except ImportError:
    pass
