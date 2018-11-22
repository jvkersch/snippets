# Example from https://ilovesymposia.com/2017/03/12/scipys-new-lowlevelcallable-is-a-game-changer/

import contextlib
import time

from scipy import ndimage as ndi
import numpy as np

from scipy import LowLevelCallable
import callable

image = np.random.random((2048, 2048))
footprint = np.array([[0, 1, 0],
                      [1, 1, 1],
                      [0, 1, 0]], dtype=bool)

c = LowLevelCallable.from_cython(callable, "nbmin")
ndi.generic_filter(image, c, footprint=footprint)
