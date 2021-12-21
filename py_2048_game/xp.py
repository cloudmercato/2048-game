import os
import numpy as np
xp = np
cp = None

if 'FORCE_NUMPY' not in os.environ:
    try:
        import cupy as cp
        xp = cp
    except ImportError:
        pass
