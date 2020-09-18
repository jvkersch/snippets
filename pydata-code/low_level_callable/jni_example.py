# Example from https://ilovesymposia.com/2017/03/12/scipys-new-lowlevelcallable-is-a-game-changer/

import contextlib
import time

from scipy import ndimage as ndi
import numpy as np

image = np.random.random((2048, 2048))
footprint = np.array([[0, 1, 0],
                      [1, 1, 1],
                      [0, 1, 0]], dtype=bool)


@contextlib.contextmanager
def timing():
    start = time.time()
    yield
    delta = time.time() - start
    print(f"Execution time: {delta:.03}s")

with timing():
    ndi.grey_erosion(image, footprint=footprint)
with timing():
    ndi.generic_filter(image, np.min, footprint=footprint)
